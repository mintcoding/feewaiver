from django.db import models
from feewaiver.main_models import CommunicationsLogEntry, UserAction, Document
from ledger.accounts.models import EmailUser, RevisionedMixin
from django.contrib.postgres.fields import ArrayField


class Participants(models.Model):
    name = models.CharField(max_length=256, blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'feewaiver'
        verbose_name_plural = 'Participants'


class Park(models.Model):
    name = models.CharField(max_length=256, blank=True, default='')
    email_list = models.CharField(max_length=256, blank=True, null=True, help_text='email addresses should be separated by semi-colons')

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'feewaiver'



class ContactDetails(RevisionedMixin):
    participants = models.ForeignKey(Participants, null=True, blank=True)
    organisation = models.CharField(max_length=256, blank=True, null=True)
    organisation_description = models.TextField(blank=True)
    contact_name = models.CharField(max_length=256, blank=True, null=True)
    postal_address = models.CharField(max_length=256, blank=True, null=True)
    suburb = models.CharField(max_length=256, blank=True, null=True)
    state = models.CharField(max_length=10, blank=True, null=True)
    postcode = models.CharField(max_length=10, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()
    # participants..?
    organisation_description = models.TextField(blank=True)

    def __str__(self):
        return 'Organisation: {}, Contact: {}'.format(self.organisation, self.contact_name)

    class Meta:
        app_label = 'feewaiver'
        verbose_name_plural = 'Contact Details'


class FeeWaiver(RevisionedMixin):
    #contact_details = models.ForeignKey(ContactDetails, null=True, blank=False, related_name='fee_waivers')
    lodgement_number = models.CharField(max_length=12, blank=True, default='')
    lodgement_date = models.DateTimeField(auto_now_add=True)
    contact_details = models.OneToOneField(ContactDetails, related_name="fee_waiver")
    fee_waiver_purpose = models.TextField(blank=True)
    #fee_waiver_description = models.TextField(blank=True)
    #date_from = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=False,verbose_name="Date from", help_text='')
    #date_to = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=False,verbose_name="Date to", help_text='')
    #parks = models.ManyToManyField(Park)
    #number_of_vehicles = models.IntegerField(default=0)
    #AGE_CHOICES = (
    #    ('15', 'Under 15 yrs'),
    #    ('24', '15-24 yrs'),
    #    ('25', '25-39 yrs'),
    #    ('40', '40-59 yrs'),
    #    ('60', '60 yrs and over')
    #)
    #age_of_participants = models.CharField(max_length=100, choices=AGE_CHOICES, null=True, blank=True,
    #                         verbose_name='Age of Participants', help_text='')


    #def __str__(self):
     #   return 'Contact details: {}, Number of vehicles: {}'.format(self.contact_details, self.number_of_vehicles)
    def __str__(self):
        return self.lodgement_number

    class Meta:
        app_label = 'feewaiver'

    #def save(self, *args, **kwargs):
    #    super(FeeWaiver, self).save(*args,**kwargs)
    #    if self.lodgement_number == '':
    #        self.lodgement_number = 'EFWR{0:06d}'.format(self.next_id)
    #        self.save()

    def save(self, *args, **kwargs):
        super(FeeWaiver, self).save(*args,**kwargs)
        if self.lodgement_number == '':
            new_lodgment_id = 'EFWR{0:06d}'.format(self.pk)
            self.lodgement_number = new_lodgment_id
            self.save()


class FeeWaiverVisit(RevisionedMixin):
    fee_waiver = models.ForeignKey(FeeWaiver, related_name="visit")
    description = models.TextField(blank=True)
    date_from = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=False,verbose_name="Date from", help_text='')
    date_to = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=False,verbose_name="Date to", help_text='')
    parks = models.ManyToManyField(Park)
    number_of_vehicles = models.IntegerField(default=0)
    camping_requested = models.BooleanField(default=False)
    AGE_CHOICES = (
        ('15', 'Under 15 yrs'),
        ('24', '15-24 yrs'),
        ('25', '25-39 yrs'),
        ('40', '40-59 yrs'),
        ('60', '60 yrs and over')
    )
    age_of_participants = models.CharField(max_length=100, choices=AGE_CHOICES, null=True, blank=True,
                             verbose_name='Age of Participants', help_text=''),
    age_of_participants_array = ArrayField(
            models.CharField(max_length=100, choices=AGE_CHOICES),
            size=5,
            default=[],
            #null=True,
            )

    def __str__(self):
        return 'Fee Waiver: {}, Visit: {}'.format(self.fee_waiver.id, self.id)
        #return 'Contact details: {}, Number of vehicles: {}'.format(self.contact_details, self.number_of_vehicles)

    class Meta:
        app_label = 'feewaiver'


class ContactDetailsDocument(Document):
    contact_details = models.ForeignKey(ContactDetails,related_name='contact_details_documents')
    #_file = models.FileField(upload_to=update_approval_doc_filename)
    _file = models.FileField(null=True)
    can_delete = models.BooleanField(default=True) # after initial submit prevent document from being deleted

    def delete(self):
        if self.can_delete:
            return super(ContactDetailsDocument, self).delete()
        logger.info('Cannot delete existing document object after Proposal has been submitted (including document submitted before Proposal pushback to status Draft): {}'.format(self.name))

    class Meta:
        app_label = 'feewaiver'


#def update_contact_details_comms_log_filename(instance, filename):
 #   return 'approvals/{}/communications/{}/{}'.format(instance.log_entry.approval.id,instance.id,filename)


class FeeWaiverLogEntry(CommunicationsLogEntry):
    fee_waiver = models.ForeignKey(FeeWaiver, related_name='comms_logs')

    class Meta:
        app_label = 'feewaiver'

    #def save(self, **kwargs):
    #    # save the application reference if the reference not provided
    #    if not self.reference:
    #        self.reference = self.approval.id
    #    super(FeeWaiverLogEntry, self).save(**kwargs)

class FeeWaiverLogDocument(Document):
    log_entry = models.ForeignKey(FeeWaiverLogEntry,related_name='documents', null=True,)
    #_file = models.FileField(upload_to=update_approval_comms_log_filename, null=True)
    _file = models.FileField(null=True)

    class Meta:
        app_label = 'feewaiver'


class FeeWaiverUserAction(UserAction):
    #ACTION_CREATE_APPROVAL = "Create approval {}"
    #ACTION_UPDATE_APPROVAL = "Update approval {}"
    #ACTION_EXPIRE_APPROVAL = "Expire approval {}"
    #ACTION_CANCEL_APPROVAL = "Cancel approval {}"
    #ACTION_SUSPEND_APPROVAL = "Suspend approval {}"
    #ACTION_REINSTATE_APPROVAL = "Reinstate approval {}"
    #ACTION_SURRENDER_APPROVAL = "Surrender approval {}"
    #ACTION_RENEW_APPROVAL = "Create renewal Proposal for approval {}"
    #ACTION_AMEND_APPROVAL = "Create amendment Proposal for approval {}"
    #ACTION_APPROVAL_PDF_VIEW ="View approval PDF for approval {}"
    #ACTION_UPDATE_NO_CHARGE_DATE_UNTIL = "'Do not charge annual site fee until' date updated to {} for approval {}"

    class Meta:
        app_label = 'feewaiver'

    @classmethod
    def log_action(cls, fee_waiver, action, user):
        #if approval.apiary_approval:
         #   action = action.replace('Approval', 'Licence').replace('approval', 'licence').replace('proposal', 'application').replace('Proposal', 'Application')
        return cls.objects.create(
            fee_waiver=fee_waiver,
            who=user,
            what=str(action)
        )

    contact_details = models.ForeignKey(FeeWaiver, related_name='action_logs')


class AssessorsGroup(models.Model):
    #site = models.OneToOneField(Site, default='1') 
    members = models.ManyToManyField(EmailUser)

    def __str__(self):
        return 'Assessors Group'

    @property
    def all_members(self):
        all_members = []
        all_members.extend(self.members.all())
        member_ids = [m.id for m in self.members.all()]
        #all_members.extend(EmailUser.objects.filter(is_superuser=True,is_staff=True,is_active=True).exclude(id__in=member_ids))
        return all_members

    @property
    def filtered_members(self):
        return self.members.all()

    class Meta:
        app_label = 'feewaiver'
        verbose_name_plural = "Assessors group"


class ApproversGroup(models.Model):
    #site = models.OneToOneField(Site, default='1') 
    members = models.ManyToManyField(EmailUser)

    def __str__(self):
        return 'Approvers Group'

    @property
    def all_members(self):
        all_members = []
        all_members.extend(self.members.all())
        member_ids = [m.id for m in self.members.all()]
        #all_members.extend(EmailUser.objects.filter(is_superuser=True,is_staff=True,is_active=True).exclude(id__in=member_ids))
        return all_members

    @property
    def filtered_members(self):
        return self.members.all()

    class Meta:
        app_label = 'feewaiver'
        verbose_name_plural = "Approvers group"

