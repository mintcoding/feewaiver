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
        FeeWaiverDTSerializer,
        FeeWaiverVisitSerializer,
        FeeWaiverLogEntrySerializer,
        FeeWaiverUserActionSerializer,
        ParticipantsSerializer,
        ParkSerializer,
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
        )
import logging
from feewaiver.emails import send_fee_waiver_received_notification
from feewaiver.main_decorators import basic_exception_handler
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
        instance = self.get_object()
        #returned_data = process_generic_document(request, instance, document_type=ContactDetailsDocument.DOC_TYPE_NAME)
        returned_data = process_generic_document(request, instance)
        if returned_data:
            return Response(returned_data)
        else:
            return Response()

    #def get_object(self):

    #    check_db_connection()
    #    try:
    #        obj = super(FeeWaiverViewSet, self).get_object()
    #    except Exception, e:
    #        # because current queryset excludes migrated licences
    #        #import ipdb; ipdb.set_trace()
    #        #obj = get_object_or_404(Proposal, id=self.kwargs['id'])
    #        obj_id = self.kwargs['id'] if 'id' in self.kwargs else self.kwargs['pk']
    #        obj = get_object_or_404(FeeWaiver, id=obj_id)
    #    return obj

    #def get_serializer_class(self):
    #    try:
    #        application_type = self.get_object().application_type.name
    #        if application_type in (ApplicationType.APIARY, ApplicationType.SITE_TRANSFER, ApplicationType.TEMPORARY_USE):
    #            return ProposalApiaryTypeSerializer
    #        else:
    #            return ProposalSerializer
    #    except serializers.ValidationError:
    #        print(traceback.print_exc())
    #        raise
    #    except ValidationError as e:
    #        if hasattr(e,'error_dict'):
    #            raise serializers.ValidationError(repr(e.error_dict))
    #        else:
    #            raise serializers.ValidationError(repr(e[0].encode('utf-8')))
    #    except Exception as e:
    #        print(traceback.print_exc())
    #        raise serializers.ValidationError(str(e))

    #@detail_route(methods=['POST'])
    #@renderer_classes((JSONRenderer,))
    #def process_document(self, request, *args, **kwargs):
    #    try:
    #        #import ipdb; ipdb.set_trace()
    #        instance = self.get_object()
    #        action = request.POST.get('action')
    #        section = request.POST.get('input_name')
    #        if action == 'list' and 'input_name' in request.POST:
    #            pass

    #        elif action == 'delete' and 'document_id' in request.POST:
    #            document_id = request.POST.get('document_id')
    #            document = instance.documents.get(id=document_id)

    #            if document._file and os.path.isfile(document._file.path) and document.can_delete:
    #                os.remove(document._file.path)

    #            document.delete()
    #            instance.save(version_comment='Approval File Deleted: {}'.format(document.name)) # to allow revision to be added to reversion history
    #            #instance.current_proposal.save(version_comment='File Deleted: {}'.format(document.name)) # to allow revision to be added to reversion history

    #        elif action == 'hide' and 'document_id' in request.POST:
    #            document_id = request.POST.get('document_id')
    #            document = instance.documents.get(id=document_id)

    #            document.hidden=True
    #            document.save()
    #            instance.save(version_comment='File hidden: {}'.format(document.name)) # to allow revision to be added to reversion history

    #        elif action == 'save' and 'input_name' in request.POST and 'filename' in request.POST:
    #            proposal_id = request.POST.get('proposal_id')
    #            filename = request.POST.get('filename')
    #            _file = request.POST.get('_file')
    #            if not _file:
    #                _file = request.FILES.get('_file')

    #            document = instance.documents.get_or_create(input_name=section, name=filename)[0]
    #            path = default_storage.save('proposals/{}/documents/{}'.format(proposal_id, filename), ContentFile(_file.read()))

    #            document._file = path
    #            #import ipdb; ipdb.set_trace()
    #            document.save()
    #            instance.save(version_comment='File Added: {}'.format(filename)) # to allow revision to be added to reversion history
    #            #instance.current_proposal.save(version_comment='File Added: {}'.format(filename)) # to allow revision to be added to reversion history

    #        return  Response( [dict(input_name=d.input_name, name=d.name,file=d._file.url, id=d.id, can_delete=d.can_delete, can_hide=d.can_hide) for d in instance.documents.filter(input_name=section, hidden=False) if d._file] )

    #    except serializers.ValidationError:
    #        print(traceback.print_exc())
    #        raise
    #    except ValidationError as e:
    #        if hasattr(e,'error_dict'):
    #            raise serializers.ValidationError(repr(e.error_dict))
    #        else:
    #            raise serializers.ValidationError(repr(e[0].encode('utf-8')))
    #    except Exception as e:
    #        print(traceback.print_exc())
    #        raise serializers.ValidationError(str(e))

#    def list(self, request, *args, **kwargs):
#        #import ipdb; ipdb.set_trace()
#        #queryset = self.get_queryset()
#        #serializer = DTProposalSerializer(queryset, many=True)
#        #import ipdb; ipdb.set_trace()
#        #serializer = DTProposalSerializer(self.get_queryset(), many=True)
#        serializer = ListProposalSerializer(self.get_queryset(), context={'request':request}, many=True)
#        return Response(serializer.data)

    #@list_route(methods=['GET',])
    #def list_paginated(self, request, *args, **kwargs):
    #    """
    #    https://stackoverflow.com/questions/29128225/django-rest-framework-3-1-breaks-pagination-paginationserializer
    #    """
    #    proposals = self.get_queryset()
    #    paginator = PageNumberPagination()
    #    #paginator = LimitOffsetPagination()
    #    paginator.page_size = 5
    #    result_page = paginator.paginate_queryset(proposals, request)
    #    serializer = ListProposalSerializer(result_page, context={'request':request}, many=True)
    #    return paginator.get_paginated_response(serializer.data)

    @list_route(methods=['GET',])
    def filter_list(self, request, *args, **kwargs):
        #import ipdb; ipdb.set_trace()
        """ Used by the internal/external dashboard filters """
        feewaiver_status = []
        data = dict(
            feewaiver_status_choices = [i[1] for i in FeeWaiver.PROCESSING_STATUS_CHOICES],
        )
        return Response(data)

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

    #@list_route(methods=['GET',])
    #def user_list(self, request, *args, **kwargs):
    #    qs = self.get_queryset().exclude(processing_status='discarded')
    #    #serializer = DTProposalSerializer(qs, many=True)
    #    serializer = ListProposalSerializer(qs,context={'request':request}, many=True)
    #    return Response(serializer.data)

    #@list_route(methods=['GET',])
    #def user_list_paginated(self, request, *args, **kwargs):
    #    """
    #    Placing Paginator class here (instead of settings.py) allows specific method for desired behaviour),
    #    otherwise all serializers will use the default pagination class

    #    https://stackoverflow.com/questions/29128225/django-rest-framework-3-1-breaks-pagination-paginationserializer
    #    """
    #    proposals = self.get_queryset().exclude(processing_status='discarded')
    #    paginator = DatatablesPageNumberPagination()
    #    paginator.page_size = proposals.count()
    #    result_page = paginator.paginate_queryset(proposals, request)
    #    serializer = ListProposalSerializer(result_page, context={'request':request}, many=True)
    #    return paginator.get_paginated_response(serializer.data)

    #@list_route(methods=['GET',])
    #def list_paginated(self, request, *args, **kwargs):
    #    """
    #    Placing Paginator class here (instead of settings.py) allows specific method for desired behaviour),
    #    otherwise all serializers will use the default pagination class

    #    https://stackoverflow.com/questions/29128225/django-rest-framework-3-1-breaks-pagination-paginationserializer
    #    """
    #    proposals = self.get_queryset()
    #    paginator = DatatablesPageNumberPagination()
    #    paginator.page_size = proposals.count()
    #    result_page = paginator.paginate_queryset(proposals, request)
    #    serializer = ListProposalSerializer(result_page, context={'request':request}, many=True)
    #    return paginator.get_paginated_response(serializer.data)

    #@detail_route(methods=['GET',])
    #def internal_proposal(self, request, *args, **kwargs):
    #    instance = self.get_object()
    #    instance.internal_view_log(request)
    #    #serializer = InternalProposalSerializer(instance,context={'request':request})
    #    serializer_class = self.internal_serializer_class()
    #    serializer = serializer_class(instance,context={'request':request})
    #    return Response(serializer.data)

    #@detail_route(methods=['GET',])
    #def internal_proposal_wrapper(self, request, *args, **kwargs):
    #    instance = self.get_object()
    #    #instance.internal_view_log(request)
    #    #serializer = InternalProposalSerializer(instance,context={'request':request})
    #    serializer_class = ProposalWrapperSerializer #self.internal_serializer_class()
    #    #serializer = serializer_class(instance,context={'request':request})
    #    serializer = serializer_class(instance)
    #    return Response(serializer.data)

    @detail_route(methods=['post'])
    @renderer_classes((JSONRenderer,))
    def submit(self, request, *args, **kwargs):
        #import ipdb; ipdb.set_trace()
        try:
            instance = self.get_object()
            if instance.apiary_group_application_type:
                save_proponent_data(instance, request, self)
            else:
                instance.submit(request, self)
                instance.tenure = search_tenure(instance)

            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
            #return redirect(reverse('external'))
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

    @detail_route(methods=['POST',])
    def assign_to(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_id = request.data.get('assessor_id',None)
            user = None
            if not user_id:
                raise serializers.ValidationError('An assessor id is required')
            try:
                user = EmailUser.objects.get(id=user_id)
            except EmailUser.DoesNotExist:
                raise serializers.ValidationError('A user with the id passed in does not exist')
            instance.assign_officer(request,user)
            #serializer = InternalProposalSerializer(instance,context={'request':request})
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
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
            serializer_class = self.internal_serializer_class()
            serializer = serializer_class(instance,context={'request':request})
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

    @detail_route(methods=['POST',])
    def proposed_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.application_type.name == ApplicationType.SITE_TRANSFER:
                #serializer = ProposedApprovalSiteTransferSerializer(data=request.data)
                serializer = ProposedApprovalSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
            else:
                serializer = ProposedApprovalSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
            instance.proposed_approval(request,serializer.validated_data)
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

    @detail_route(methods=['POST',])
    def approval_level_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance = instance.assing_approval_level_document(request)
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

    @detail_route(methods=['POST',])
    def approval_level_comment(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance = instance.save_approval_level_comment(request)
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

    @detail_route(methods=['POST',])
    def final_approval(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = ProposedApprovalSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.final_approval(request,serializer.validated_data)
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

    @detail_route(methods=['POST',])
    def proposed_decline(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = PropedDeclineSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.proposed_decline(request,serializer.validated_data)
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

    @detail_route(methods=['POST',])
    def final_decline(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = PropedDeclineSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance.final_decline(request,serializer.validated_data)
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

    @detail_route(methods=['post'])
    @renderer_classes((JSONRenderer,))
    def assessor_save(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            save_assessor_data(instance,request,self)
            return redirect(reverse('external'))
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
            waiver_serializer = FeeWaiverSerializer(instance)
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
                return Response(waiver_serializer.data)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    # def retrieve(self, request, *args, **kwargs):
    #     pass

    #def update(self, request, *args, **kwargs):
    #    """
    #    This function might not be used anymore
    #    The function 'draft()' is used rather than this update()
    #    """
    #    try:
    #        http_status = status.HTTP_200_OK
    #        application_type = ApplicationType.objects.get(id=request.data.get('application'))

    #        # When there is a parameter named 'application_type_str', we may need to update application_type
    #        application_type_str = request.data.get('application_type_str', None)
    #        if application_type_str == 'temporary_use':
    #            application_type = ApplicationType.objects.get(name=ApplicationType.TEMPORARY_USE)
    #        elif application_type_str == 'site_transfer':
    #            application_type = ApplicationType.objects.get(name=ApplicationType.SITE_TRANSFER)

    #        if application_type.name == ApplicationType.APIARY:
    #            pass
    #            # TODO Update new apiary application

    #        elif application_type.name == ApplicationType.TEMPORARY_USE:
    #            # Proposal obj should not be changed
    #            # Only ProposalApiaryTemporaryUse object needs to be updated
    #            apiary_temporary_use_obj = ProposalApiaryTemporaryUse.objects.get(id=request.data.get('apiary_temporary_use')['id'])
    #            apiary_temporary_use_data = request.data.get('apiary_temporary_use')
    #            update_proposal_apiary_temporary_use(apiary_temporary_use_obj, apiary_temporary_use_data)

    #            proposal_obj = self.get_object()
    #            serializer = ProposalSerializer(proposal_obj)
    #            return Response(serializer.data)

    #        elif application_type.name == ApplicationType.SITE_TRANSFER:
    #            pass
    #            # TODO update Site Transfer Application

    #        instance = self.get_object()
    #        serializer = SaveProposalSerializer(instance, data=request.data)
    #        serializer.is_valid(raise_exception=True)
    #        self.perform_update(serializer)
    #        return Response(serializer.data)
    #    except Exception as e:
    #        print(traceback.print_exc())
    #        raise serializers.ValidationError(str(e))

    def destroy(self, request,*args,**kwargs):
        try:
            http_status = status.HTTP_200_OK
            instance = self.get_object()
            serializer = SaveProposalSerializer(instance,{'processing_status':'discarded', 'previous_application': None},partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data,status=http_status)
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


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

