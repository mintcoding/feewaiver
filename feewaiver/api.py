import re
import traceback
import os

import json

import pytz
from ledger.settings_base import TIME_ZONE, DATABASES
from django.db.models import Q
from django.db import transaction
from django.core.exceptions import ValidationError
from rest_framework import viewsets, serializers, status, views
from rest_framework.decorators import detail_route, list_route, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from ledger.accounts.models import EmailUser
from datetime import datetime

from django.http import HttpResponse#, JsonResponse, Http404
from feewaiver import settings
#from disturbance.components.approvals.email import send_contact_licence_holder_email

from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
#from disturbance.components.main.models import ApplicationType, ApiaryGlobalSettings
from feewaiver.serializers import (
        ContactDetailsSerializer,
        FeeWaiverSerializer,
        ContactDetailsSaveSerializer,
        FeeWaiverSaveSerializer,
        FeeWaiverDTSerializer,
        FeeWaiverVisitSerializer,
        FeeWaiverVisitSaveSerializer,
        FeeWaiverLogEntrySerializer,
        FeeWaiverUserActionSerializer,
        ParticipantsSerializer,
        ParkSerializer,
        TemporaryDocumentCollectionSerializer,
)
from feewaiver.models import (
        ContactDetails,
        ContactDetailsDocument,
        FeeWaiver,
        FeeWaiverVisit,
        FeeWaiverLogEntry,
        FeeWaiverUserAction,
        Participants,
        Park,
)
from feewaiver.helpers import is_customer, is_internal, is_feewaiver_admin
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework.pagination import PageNumberPagination
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer
from feewaiver.process_document import (
        process_generic_document,
        save_contact_details_document_obj,
        save_default_document_obj,
        )
import logging
from feewaiver.emails import (
        send_fee_waiver_received_notification,
        send_workflow_notification,
        send_approver_notification,
        )
from feewaiver.main_decorators import basic_exception_handler
from feewaiver.main_models import TemporaryDocumentCollection
from feewaiver.process_document import save_document, cancel_document, delete_document
logger = logging.getLogger(__name__)


class GetEmptyList(views.APIView):
    renderer_classes = [JSONRenderer, ]

    def get(self, request, format=None):
        return Response([])

#class DatatablesFilterBackend(BaseFilterBackend):
#
#	def filter_queryset(self, request, queryset, view):
#		queryset = super(DatatablesFilterBackend, self).filter_queryset(request, queryset, view)
#		import ipdb; ipdb.set_trace()
#		return queryset

class FeeWaiverFilterBackend(DatatablesFilterBackend):
    """
    Custom filters
    """

    def filter_queryset(self, request, queryset, view):
        #import ipdb; ipdb.set_trace()
        #print(request.GET)
        total_count = queryset.count()

        def get_choice(status, choices=FeeWaiver.PROCESSING_STATUS_CHOICES):
            for i in choices:
                if i[1]==status:
                    return i[0]
            return None

        processing_status = request.GET.get('processing_status')
        if processing_status and not processing_status.lower() == 'all':
            processing_status = get_choice(processing_status, FeeWaiver.PROCESSING_STATUS_CHOICES)
            queryset = queryset.filter(processing_status=processing_status)

        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        if date_from:
            queryset = queryset.filter(lodgement_date__gte=date_from)
        if date_to:
            queryset = queryset.filter(lodgement_date__lte=date_to)

        getter = request.query_params.get
        fields = self.get_fields(getter)
        ordering = self.get_ordering(getter, fields)
        queryset = queryset.order_by(*ordering)
        if len(ordering):
            #for num, item in enumerate(ordering):
                #if item == 'status__name':
                 #   ordering[num] = 'status'
                #elif item == '-status__name':
                 #   ordering[num] = '-status'
            queryset = queryset.order_by(*ordering)

        #queryset = super(FeeWaiverFilterBackend, self).filter_queryset(request, queryset, view)
        setattr(view, '_datatables_total_count', total_count)
        return queryset

class FeeWaiverRenderer(DatatablesRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        #import ipdb; ipdb.set_trace()
        if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
            data['recordsTotal'] = renderer_context['view']._datatables_total_count
            #data.pop('recordsTotal')
            #data.pop('recordsFiltered')
        return super(FeeWaiverRenderer, self).render(data, accepted_media_type, renderer_context)

#from django.utils.decorators import method_decorator
#from django.views.decorators.cache import cache_page
class FeeWaiverPaginatedViewSet(viewsets.ModelViewSet):
    #import ipdb; ipdb.set_trace()
    #queryset = Proposal.objects.all()
    #filter_backends = (DatatablesFilterBackend,)
    filter_backends = (FeeWaiverFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (FeeWaiverRenderer,)
    queryset = FeeWaiver.objects.none()
    serializer_class = FeeWaiverDTSerializer
    #serializer_class = DTProposalSerializer
    page_size = 10

#    @method_decorator(cache_page(60))
#    def dispatch(self, *args, **kwargs):
#        return super(ListProposalViewSet, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        #user = self.request.user
        #import ipdb; ipdb.set_trace()
        if is_internal(self.request): #user.is_authenticated():
            #return Proposal.objects.all().order_by('-id')
            return FeeWaiver.objects.all()
        #elif is_customer(self.request):
            #user_orgs = [org.id for org in user.disturbance_organisations.all()]
            #return Proposal.objects.filter( Q(applicant_id__in = user_orgs) | Q(submitter = user) | Q(proxy_applicant = user))
        return Feewaiver.objects.none()

#    def filter_queryset(self, request, queryset, view):
#        return self.filter_backends[0]().filter_queryset(self.request, queryset, view)
        #return super(ProposalPaginatedViewSet, self).filter_queryset(request, queryset, view)

#    def list(self, request, *args, **kwargs):
#        response = super(ProposalPaginatedViewSet, self).list(request, args, kwargs)
#
#        # Add extra data to response.data
#        #response.data['regions'] = self.get_queryset().filter(region__isnull=False).values_list('region__name', flat=True).distinct()
#        return response

    @list_route(methods=['GET',])
    def feewaiver_internal(self, request, *args, **kwargs):
        """
        Used by the internal dashboard

        http://localhost:8499/api/proposal_paginated/proposal_paginated_internal/?format=datatables&draw=1&length=2
        """
        #template_group = get_template_group(request)
        #import ipdb; ipdb.set_trace()
        #if template_group == 'apiary':
        #    #qs = self.get_queryset().filter(application_type__apiary_group_application_type=True)
        #    qs = self.get_queryset().filter(
        #            application_type__name__in=[ApplicationType.APIARY, ApplicationType.SITE_TRANSFER, ApplicationType.TEMPORARY_USE]
        #            ).exclude(processing_status='discarded')
        #else:
        #    if is_das_apiary_admin(self.request):
        #        qs = self.get_queryset()
        #    else:
        #        qs = self.get_queryset().exclude(
        #                application_type__name__in=[ApplicationType.APIARY, ApplicationType.SITE_TRANSFER, ApplicationType.TEMPORARY_USE]
        #                ).exclude(processing_status='discarded')
        qs = self.get_queryset()
        qs = self.filter_queryset(qs)

        # on the internal organisations dashboard, filter the Proposal/Approval/Compliance datatables by applicant/organisation
        #applicant_id = request.GET.get('org_id')
        #if applicant_id:
         #   qs = qs.filter(applicant_id=applicant_id)

        self.paginator.page_size = qs.count()
        #import ipdb; ipdb.set_trace()
        result_page = self.paginator.paginate_queryset(qs, request)
        #serializer = FeeWaiverSerializer(result_page, context={
         #   'request':request,
          #  }, many=True)
        serializer = FeeWaiverDTSerializer(result_page, context={
            'request':request,
            }, many=True)
        #serializer = DTProposalSerializer(result_page, context={'request':request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class FeeWaiverViewSet(viewsets.ModelViewSet):
    #import ipdb; ipdb.set_trace()
    #queryset = Proposal.objects.all()
    queryset = FeeWaiver.objects.none()
    serializer_class = FeeWaiverSerializer

    def get_queryset(self):
        user = self.request.user
        #import ipdb; ipdb.set_trace()
        if is_internal(self.request): #user.is_authenticated():
            return FeeWaiver.objects.all()
        #elif is_customer(self.request):
        #    user_orgs = [org.id for org in user.disturbance_organisations.all()]
        #    #queryset =  Proposal.objects.filter( Q(applicant_id__in = user_orgs) | Q(submitter = user) )
        #    queryset =  Proposal.objects.filter(region__isnull=False).filter( Q(applicant_id__in = user_orgs) | Q(submitter = user) )
        #    return queryset
        #logger.warn("User is neither customer nor internal user: {} <{}>".format(user.get_full_name(), user.email))
        return FeeWaiver.objects.none()

    @detail_route(methods=['POST'])
    @renderer_classes((JSONRenderer,))
    @basic_exception_handler
    def process_contact_details_document(self, request, *args, **kwargs):
        #import ipdb; ipdb_set_trace()
        instance = self.get_object()
        #returned_data = process_generic_document(request, instance, document_type=ContactDetailsDocument.DOC_TYPE_NAME)
        #import ipdb; ipdb.set_trace()
        returned_data = process_generic_document(request, instance.contact_details)
        if returned_data:
            return Response(returned_data)
        else:
            return Response()

    @detail_route(methods=['POST'])
    @renderer_classes((JSONRenderer,))
    def process_comms_log_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            returned_data = process_generic_document(request, instance, document_type='comms_log')
            if returned_data:
                return Response(returned_data)
            else:
                return Response()

        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


    @detail_route(methods=['GET',])
    def assign_request_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.assign_officer(request,request.user)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            #serializer_class = self.internal_serializer_class()
            serializer = FeeWaiverSerializer(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @list_route(methods=['GET',])
    def filter_list(self, request, *args, **kwargs):
        #import ipdb; ipdb.set_trace()
        """ Used by the internal/external dashboard filters """
        feewaiver_status = []
        data = dict(
            feewaiver_status_choices = [i[1] for i in FeeWaiver.PROCESSING_STATUS_CHOICES],
        )
        return Response(data)

    @list_route(methods=['GET',])
    def camping_choices(self, request, *args, **kwargs):
        #import ipdb; ipdb.set_trace()
        camping_choices = []
        for choice in FeeWaiverVisit.CAMPING_CHOICES:
            camping_choices.append({choice[0]: choice[1]})
        return Response(camping_choices)

    @detail_route(methods=['GET',])
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = FeeWaiverUserActionSerializer(qs,many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',])
    def comms_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.comms_logs.all()
            serializer = FeeWaiverLogEntrySerializer(qs,many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',])
    @renderer_classes((JSONRenderer,))
    def add_comms_log(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                request.data['fee_waiver'] = u'{}'.format(instance.id)
                #request.data['staff'] = u'{}'.format(request.user.id)
                serializer = FeeWaiverLogEntrySerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                comms = serializer.save()
                # Save the files
                for f in request.FILES:
                    document = comms.documents.create()
                    document.name = str(request.FILES[f])
                    document._file = request.FILES[f]
                    document.save()
                # End Save Documents

                return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


    @detail_route(methods=['POST',])
    def assign_to(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_id = request.data.get('assigned_officer_id',None)
            user = None
            if not user_id:
                raise serializers.ValidationError('An assigned officer id is required')
            try:
                user = EmailUser.objects.get(id=user_id)
            except EmailUser.DoesNotExist:
                raise serializers.ValidationError('A user with the id passed in does not exist')
            instance.assign_officer(request,user)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            #serializer_class = self.internal_serializer_class()
            serializer = FeeWaiverSerializer(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET',])
    def unassign(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.unassign(request)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            #serializer_class = self.internal_serializer_class()
            serializer = FeeWaiverSerializer(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST',])
    def switch_status(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            status = request.data.get('status')
            approver_comment = request.data.get('approver_comment')
            if not status:
                raise serializers.ValidationError('Status is required')
            else:
                if not status in ['with_assessor','with_assessor_requirements','with_approver']:
                    raise serializers.ValidationError('The status provided is not allowed')
            instance.move_to_status(request,status, approver_comment)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


    @detail_route(methods=['POST'])
    @renderer_classes((JSONRenderer,))
    def workflow_action(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                #import ipdb; ipdb.set_trace()
                instance = self.get_object()
                action = request.data.get("workflow_type")
                email_subject = request.data.get("email_subject")
                if action == 'propose_issue':
                    instance.propose_issue(request)
                if action == 'propose_concession':
                    instance.propose_concession(request)
                if action == 'propose_decline':
                    instance.propose_decline(request)
                #if action == 'issue':
                #    instance.issue(request)
                #    instance.generate_doc()
                #if action == 'issue_concession':
                #    instance.issue_concession(request)
                #if action == 'decline':
                #    instance.decline(request)
                if action == 'return_to_assessor':
                    instance.return_to_assessor(request)
                comms_log_id = request.data.get('comms_log_id')
                workflow_entry = None
                if comms_log_id and comms_log_id != 'null':
                    workflow_entry = instance.comms_logs.get(
                            id=comms_log_id)
                #else:
                 #   workflow_entry = self.add_comms_log(request, instance, workflow=True)

                # send email
                send_workflow_notification(instance,request, action, email_subject, workflow_entry)
                return Response()

        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST'])
    @renderer_classes((JSONRenderer,))
    def final_approval(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                #import ipdb; ipdb.set_trace()
                instance = self.get_object()
                action = request.data.get("approval_type")
                #email_subject = request.data.get("email_subject")
                if action == 'issue':
                    instance.issue(request)
                    instance.generate_doc()
                if action == 'issue_concession':
                    instance.issue_concession(request)
                    instance.generate_doc()
                if action == 'decline':
                    instance.decline(request)

                # send email
                send_approver_notification(instance, request, action)
                return Response()

        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST'])
    @renderer_classes((JSONRenderer,))
    def assessor_save(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                #import ipdb; ipdb.set_trace()
                instance = self.get_object()
                #save_assessor_data(instance,request,self)
                #return redirect(reverse('external'))
                contact_details_data = request.data.get('contact_details')
                contact_serializer = ContactDetailsSaveSerializer(instance.contact_details, data=contact_details_data)
                contact_serializer.is_valid(raise_exception=True)
                contact_details_obj = contact_serializer.save()

                fee_waiver_data = request.data.get('fee_waiver')
                #print("fee_waiver_data")
                #print(fee_waiver_data)
                #fee_waiver_data.update({'contact_details_id': contact_details_obj.id})
                waiver_serializer = FeeWaiverSaveSerializer(instance, data=fee_waiver_data)
                #waiver_serializer = FeeWaiverSerializer(data=fee_waiver_data,context={'request':request})
                waiver_serializer.is_valid(raise_exception=True)
                fee_waiver_obj = waiver_serializer.save()

                visits_data = request.data.get('visits')
                for visit in visits_data:
                    #visit['fee_waiver_id'] = fee_waiver_obj.id
                    visit_obj = FeeWaiverVisit.objects.get(id=visit['id'])
                    visit_serializer = FeeWaiverVisitSaveSerializer(visit_obj, data=visit)
                    visit_serializer.is_valid(raise_exception=True)
                    visit_obj = visit_serializer.save()
                    # add parks
                    parks_data = visit.get('selected_park_ids')
                    if parks_data:
                        for park_id in parks_data:
                            if park_id not in visit_obj.parks.all().values_list('id', flat=True):
                                visit_obj.parks.add(Park.objects.get(id=park_id))

                instance.log_user_action(
                    FeeWaiverUserAction.ACTION_SAVE.format(instance.lodgement_number, request.user.get_full_name()),
                    request)
                return Response()
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['get'])
    @renderer_classes((JSONRenderer,))
    def feewaiver_contactdetails_pack(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            contact_serializer = ContactDetailsSerializer(instance.contact_details)
            waiver_serializer = FeeWaiverSerializer(instance, context={'request': request})
            return Response({
                "contact_details": contact_serializer.data,
                "fee_waiver": waiver_serializer.data,
                })
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                #http_status = status.HTTP_200_OK
                contact_details_data = request.data.get('contact_details')
                contact_serializer = ContactDetailsSerializer(data=contact_details_data)
                contact_serializer.is_valid(raise_exception=True)
                contact_details_obj = contact_serializer.save()

                fee_waiver_data = request.data.get('fee_waiver')
                fee_waiver_data.update({'contact_details_id': contact_details_obj.id})
                waiver_serializer = FeeWaiverSerializer(data=fee_waiver_data)
                #waiver_serializer = FeeWaiverSerializer(data=fee_waiver_data,context={'request':request})
                waiver_serializer.is_valid(raise_exception=True)
                fee_waiver_obj = waiver_serializer.save()
                # add visits
                #import ipdb; ipdb.set_trace();
                visits_data = request.data.get('visits')
                for visit in visits_data:
                    visit['fee_waiver_id'] = fee_waiver_obj.id
                    visit_serializer = FeeWaiverVisitSerializer(data=visit)
                    visit_serializer.is_valid(raise_exception=True)
                    visit_obj = visit_serializer.save()
                    # add parks
                    parks_data = visit.get('selected_park_ids')
                    if parks_data:
                        for park_id in parks_data:
                            visit_obj.parks.add(Park.objects.get(id=park_id))
                # send email
                send_fee_waiver_received_notification(fee_waiver_obj,request)
                #workflow_entry = self.add_comms_log(request, instance, workflow=True)
                #import ipdb; ipdb.set_trace()
                temporary_document_collection_id = request.data.get('temporary_document_collection_id')
                if temporary_document_collection_id:
                    temp_doc_collection, created = TemporaryDocumentCollection.objects.get_or_create(
                            id=temporary_document_collection_id)
                    if temp_doc_collection:
                        for doc in temp_doc_collection.documents.all():
                            #save_contact_details_document_obj(contact_details_obj, doc)
                            save_default_document_obj(contact_details_obj, doc)
                        temp_doc_collection.delete()

                return Response(waiver_serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    #def retrieve(self, request, *args, **kwargs):
     #   import ipdb; ipdb.set_trace()
      #  pass


    #def destroy(self, request,*args,**kwargs):
    #    try:
    #        http_status = status.HTTP_200_OK
    #        instance = self.get_object()
    #        serializer = SaveProposalSerializer(instance,{'processing_status':'discarded', 'previous_application': None},partial=True)
    #        serializer.is_valid(raise_exception=True)
    #        self.perform_update(serializer)
    #        return Response(serializer.data,status=http_status)
    #    except Exception as e:
    #        print(traceback.print_exc())
    #        raise serializers.ValidationError(str(e))


class SearchKeywordsView(views.APIView):
    renderer_classes = [JSONRenderer,]
    def post(self,request, format=None):
        qs = []
        searchWords = request.data.get('searchKeywords')
        searchProposal = request.data.get('searchProposal')
        searchApproval = request.data.get('searchApproval')
        searchCompliance = request.data.get('searchCompliance')
        if searchWords:
            qs= searchKeyWords(searchWords, searchProposal, searchApproval, searchCompliance)
        #queryset = list(set(qs))
        serializer = SearchKeywordSerializer(qs, many=True)
        return Response(serializer.data)


class SearchReferenceView(views.APIView):
    renderer_classes = [JSONRenderer,]
    def post(self,request, format=None):
        try:
            qs = []
            reference_number = request.data.get('reference_number')
            if reference_number:
                qs= search_reference(reference_number)
            #queryset = list(set(qs))
            serializer = SearchReferenceSerializer(qs)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e,'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                print(e)
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class ParticipantsViewSet(viewsets.ModelViewSet):
    #import ipdb; ipdb.set_trace()
    #queryset = Proposal.objects.all()
    queryset = Participants.objects.none()
    serializer_class = ParticipantsSerializer

    def get_queryset(self):
        user = self.request.user
        #import ipdb; ipdb.set_trace()
        if is_internal(self.request): #user.is_authenticated():
            return Participants.objects.all()
        return Participants.objects.none()

    @list_route(methods=['GET',])
    def participants_list(self, request, *args, **kwargs):
        #qs = Participants.objects.filter().values_list('name', flat=True)
        serializer = ParticipantsSerializer(Participants.objects.all(), many=True)
        return Response(serializer.data)


class ParkViewSet(viewsets.ModelViewSet):
    #import ipdb; ipdb.set_trace()
    #queryset = Proposal.objects.all()
    queryset = Park.objects.none()
    serializer_class = ParkSerializer

    def get_queryset(self):
        user = self.request.user
        #import ipdb; ipdb.set_trace()
        if is_internal(self.request): #user.is_authenticated():
            return Park.objects.all()
        return Park.objects.none()

    @list_route(methods=['GET',])
    def parks_list(self, request, *args, **kwargs):
        #qs = Participants.objects.filter().values_list('name', flat=True)
        serializer = ParkSerializer(Park.objects.all(), many=True)
        return Response(serializer.data)


class TemporaryDocumentCollectionViewSet(viewsets.ModelViewSet):
    queryset = TemporaryDocumentCollection.objects.all()
    serializer_class = TemporaryDocumentCollectionSerializer

    #def get_queryset(self):
    #    if is_internal(self.request):
    #        return TemporaryDocumentCollection.objects.all()
    #    return TemporaryDocumentCollection.objects.none()

    def create(self, request, *args, **kwargs):
        print("create temp doc coll")
        print(request.data)
        try:
            with transaction.atomic():
                serializer = TemporaryDocumentCollectionSerializer(
                        data=request.data, 
                        )
                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    instance = serializer.save()
                    save_document(request, instance, comms_instance=None, document_type=None)

                    return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                raise serializers.ValidationError(repr(e[0].encode('utf-8')))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST'])
    @renderer_classes((JSONRenderer,))
    # Designed for uploading comms_log files within "create" modals when no parent entity instance yet exists
    # response returned to compliance_file.vue
    def process_temp_comms_log_document(self, request, *args, **kwargs):
        print("process_temp_comms_log_document")
        print(request.data)
        try:
            instance = self.get_object()
            action = request.data.get('action')
            #comms_instance = None

            if action == 'list':
                pass

            elif action == 'delete':
                delete_document(request, instance, comms_instance=None, document_type=None)

            elif action == 'cancel':
                cancel_document(request, instance, comms_instance=None, document_type=None)

            elif action == 'save':
                save_document(request, instance, comms_instance=None, document_type=None)

            returned_file_data = [dict(
                        file=d._file.url,
                        id=d.id,
                        name=d.name,
                        ) for d in instance.documents.all() if d._file]
            return Response({'filedata': returned_file_data})

        except Exception as e:
            print(traceback.print_exc())
            raise e

    @detail_route(methods=['POST'])
    @renderer_classes((JSONRenderer,))
    # Designed for uploading comms_log files within "create" modals when no parent entity instance yet exists
    # response returned to compliance_file.vue
    def process_temp_document(self, request, *args, **kwargs):
        print("process_temp_document")
        print(request.data)
        try:
            #import ipdb; ipdb.set_trace()
            instance = self.get_object()
            action = request.data.get('action')
            #comms_instance = None

            if action == 'list':
                pass

            elif action == 'delete':
                delete_document(request, instance, comms_instance=None, document_type=None)

            elif action == 'cancel':
                cancel_document(request, instance, comms_instance=None, document_type=None)

            elif action == 'save':
                save_document(request, instance, comms_instance=None, document_type=None)

            returned_file_data = [dict(
                        file=d._file.url,
                        id=d.id,
                        name=d.name,
                        ) for d in instance.documents.all() if d._file]
            return Response({'filedata': returned_file_data})

        except Exception as e:
            print(traceback.print_exc())
            raise e

    #def retrieve(self, request, *args, **kwargs):
     #   import ipdb; ipdb.set_trace()
      #  pass
