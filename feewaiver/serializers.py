from ledger.accounts.models import EmailUser
from rest_framework import serializers

from feewaiver.models import (
        ContactDetails, 
        FeeWaiver,
        FeeWaiverVisit,
        FeeWaiverUserAction,
        FeeWaiverLogEntry,
        Participants,
        Park,
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
    participants_id = serializers.IntegerField(write_only=True)
    participants_code = serializers.SerializerMethodField()
    #        required=True, write_only=True, allow_null=False)

    class Meta:
        model = ContactDetails
        fields = (
                'id',
                'organisation',
                'organisation_description',
                'contact_name',
                'postal_address',
                'suburb',                     
                'state',                     
                'postcode',                     
                'phone',
                'email',
                'participants_id',
                'participants_code',
                'organisation_description'
                )
        read_only_fields = (
            'id',
        )

    def get_participants_code(self,obj):
        return obj.participants_id

class ParkSerializer(serializers.ModelSerializer):

    class Meta:
        model = Park
        fields = (
                'id',
                'name',
                )
        read_only_fields = (
            'id',
        )


class FeeWaiverVisitSerializer(serializers.ModelSerializer):
    #fee_waiver = FeeWaiverSerializer()
    selected_park_ids = serializers.SerializerMethodField()
    fee_waiver_id = serializers.IntegerField(
            required=True, write_only=True, allow_null=False)


    class Meta:
        model = FeeWaiverVisit
        fields = (
                'id',
                'fee_waiver_id',
                'description',     
                'camping_requested',
                'date_from',     
                'date_to',     
                'selected_park_ids',    
                'number_of_vehicles',     
                'age_of_participants', 
                )
        read_only_fields = (
            'id',
        )

    def get_selected_park_ids(self, obj):
        park_id_list = []
        for park in obj.parks.all():
            park_id_list.append(str(park.id))
        return park_id_list


class FeeWaiverSerializer(serializers.ModelSerializer):
    visits = serializers.SerializerMethodField()
    contact_details_id = serializers.IntegerField(
            required=True, write_only=True, allow_null=False)


    class Meta:
        model = FeeWaiver
        fields = (
                'id',
                'lodgement_number',
                'lodgement_date',
                'contact_details_id',     
                'fee_waiver_purpose',     
                'visits',
                )
        read_only_fields = (
            'id',
            'lodgement_number',
            'lodgement_date',
        )

    def get_visits(self, obj):
        visits = []
        for visit in obj.visit.all():
            visits.append(FeeWaiverVisitSerializer(visit).data)
        return visits


class FeeWaiverDTSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeeWaiver
        fields = (
                'id',
                'lodgement_number',
                #'submitter',
                #'status',
                'lodgement_date',
                #document,
                #assigned_to,
                )
        read_only_fields = (
            'id',
        )


class ParticipantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Participants
        fields = (
                'id',
                'name',
                )
        read_only_fields = (
            'id',
        )


