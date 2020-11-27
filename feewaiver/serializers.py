from ledger.accounts.models import EmailUser
from rest_framework import serializers

from feewaiver.models import (
        ContactDetails, 
        FeeWaiver,
        FeeWaiverUserAction,
        FeeWaiverLogEntry,
        )
#from disturbance.components.organisations.models import (
 #                               Organisation
  #                          )
from feewaiver.main_serializers import CommunicationLogEntrySerializer
from rest_framework import serializers


class EmailUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = EmailUser
        fields = (
                'id',
                'email',
                'first_name',
                'last_name',
                'title',
                'organisation',
                'name'
                )

    def get_name(self, obj):
        return obj.get_full_name()


class FeeWaiverUserActionSerializer(serializers.ModelSerializer):
    who = serializers.CharField(source='who.get_full_name')
    class Meta:
        model = FeeWaiverUserAction
        fields = '__all__'

class FeeWaiverLogEntrySerializer(CommunicationLogEntrySerializer):
    documents = serializers.SerializerMethodField()
    class Meta:
        model = FeeWaiverLogEntry
        fields = '__all__'
        read_only_fields = (
            'customer',
        )

    def get_documents(self,obj):
        return [[d.name,d._file.url] for d in obj.documents.all()]

class ContactDetailsSerializer(serializers.ModelSerializer):
#    readonly = serializers.SerializerMethodField(read_only=True)
#    documents_url = serializers.SerializerMethodField()
#    proposal_type = serializers.SerializerMethodField()
#    allowed_assessors = EmailUserSerializer(many=True)
#
#    get_history = serializers.ReadOnlyField()


    class Meta:
        model = ContactDetails
        fields = (
                'organisation',
                'contact_name',
                'postal_address',
                'suburb',                     
                'state',                     
                'postcode',                     
                'phone',
                'email',
                # participants..?
                'organisation_description'
                )
#        read_only_fields=('documents',)
#
#    def get_documents_url(self,obj):
#        return '/media/proposals/{}/documents/'.format(obj.id)
#
#    def get_readonly(self,obj):
#        return False
#
#    def get_processing_status(self,obj):
#        return obj.get_processing_status_display()
#
#    def get_review_status(self,obj):
#        return obj.get_review_status_display()
#
#    def get_customer_status(self,obj):
#        return obj.get_customer_status_display()
#
#    def get_proposal_type(self,obj):
#        return obj.get_proposal_type_display()
#
class FeeWaiverSerializer(serializers.ModelSerializer):
#    readonly = serializers.SerializerMethodField(read_only=True)
#    documents_url = serializers.SerializerMethodField()
#    proposal_type = serializers.SerializerMethodField()
#    allowed_assessors = EmailUserSerializer(many=True)
#
#    get_history = serializers.ReadOnlyField()


    class Meta:
        model = FeeWaiver
        fields = (
                'contact_details_id',     
                'fee_waiver_purpose',     
                'fee_waiver_description',     
                'date_from',     
                'date_to',     
                # park,    
                'number_of_vehicles',     
                'age_of_participants', 
                )
                    
