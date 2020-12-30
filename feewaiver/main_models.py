from __future__ import unicode_literals
import os

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.utils.encoding import python_2_unicode_compatible
from django.core.exceptions import ValidationError
#from ledger.accounts.models import EmailUser, Document, RevisionedMixin
from ledger.accounts.models import EmailUser, RevisionedMixin
from django.contrib.postgres.fields.jsonb import JSONField


@python_2_unicode_compatible
class UserAction(models.Model):
    who = models.ForeignKey(EmailUser, null=False, blank=False)
    when = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    what = models.TextField(blank=False)

    def __str__(self):
        return "{what} ({who} at {when})".format(
            what=self.what,
            who=self.who,
            when=self.when
        )

    class Meta:
        abstract = True
        app_label = 'feewaiver'


class CommunicationsLogEntry(models.Model):
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone Call'),
        ('mail', 'Mail'),
        ('person', 'In Person'),
        ('onhold', 'On Hold'),
        ('onhold_remove', 'Remove On Hold'),
        ('with_qaofficer', 'With QA Officer'),
        ('with_qaofficer_completed', 'QA Officer Completed'),
        ('referral_complete','Referral Completed'),
    ]
    DEFAULT_TYPE = TYPE_CHOICES[0][0]

    #to = models.CharField(max_length=200, blank=True, verbose_name="To")
    to = models.TextField(blank=True, verbose_name="To")
    fromm = models.CharField(max_length=200, blank=True, verbose_name="From")
    #cc = models.CharField(max_length=200, blank=True, verbose_name="cc")
    cc = models.TextField(blank=True, verbose_name="cc")

    type = models.CharField(max_length=35, choices=TYPE_CHOICES, default=DEFAULT_TYPE)
    reference = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=200, blank=True, verbose_name="Subject / Description")
    text = models.TextField(blank=True)

    customer = models.ForeignKey(EmailUser, null=True, related_name='+')
    staff = models.ForeignKey(EmailUser, null=True, related_name='+')

    created = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    class Meta:
        app_label = 'feewaiver'


@python_2_unicode_compatible
class Document(models.Model):
    name = models.CharField(max_length=255, blank=True,
                            verbose_name='name', help_text='')
    description = models.TextField(blank=True,
                                   verbose_name='description', help_text='')
    uploaded_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'feewaiver'
        abstract = True

    @property
    def path(self):
        #return self.file.path
        #return self._file.path
        #comment above line to fix the error "The '_file' attribute has no file associated with it." when adding comms log entry.
        if self._file:
            return self._file.path
        else:
            return ''

    @property
    def filename(self):
        return os.path.basename(self.path)

    def __str__(self):
        return self.name or self.filename

class GlobalSettings(models.Model):
    KEY_FEEWAIVER_TEMPLATE_FILE = 'feewaiver_template_file'
    keys = (
            (KEY_FEEWAIVER_TEMPLATE_FILE, 'Feewaiver template file'),
            )
    default_values = (
            (KEY_FEEWAIVER_TEMPLATE_FILE, ''),
            )
    key = models.CharField(max_length=255, choices=keys, blank=False, null=False,)
    value = models.CharField(max_length=255)
    _file = models.FileField(upload_to='feewaiver_template', null=True, blank=True)

    class Meta:
        app_label = 'feewaiver'
        verbose_name_plural = "Global Settings"


@python_2_unicode_compatible
class SystemMaintenance(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def duration(self):
        """ Duration of system maintenance (in mins) """
        return int( (self.end_date - self.start_date).total_seconds()/60.) if self.end_date and self.start_date else ''
        #return (datetime.now(tz=tz) - self.start_date).total_seconds()/60.
    duration.short_description = 'Duration (mins)'

    class Meta:
        app_label = 'feewaiver'
        verbose_name_plural = "System maintenance"

    def __str__(self):
        return 'System Maintenance: {} ({}) - starting {}, ending {}'.format(self.name, self.description, self.start_date, self.end_date)

class UserSystemSettings(models.Model):
    one_row_per_park = models.BooleanField(default=False) #Setting for user if they want to see Payment (Park Entry Fees Dashboard) by one row per park or one row per booking
    #user = models.ForeignKey(EmailUser, unique=True, related_name='system_settings')
    user = models.OneToOneField(EmailUser, related_name='system_settings')


    class Meta:
        app_label = 'feewaiver'
        verbose_name_plural = "User System Settings"


class TemporaryDocumentCollection(models.Model):
    # input_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'feewaiver'


# temp document obj for generic file upload component
class TemporaryDocument(Document):
    temp_document_collection = models.ForeignKey(
        TemporaryDocumentCollection,
        related_name='documents')
    _file = models.FileField(max_length=255)

    # input_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        app_label = 'feewaiver'

import reversion
#reversion.register(Region, follow=['districts'])
#reversion.register(District, follow=['parks'])
#reversion.register(AccessType, follow=['park_set', 'proposalparkaccess_set', 'vehicles'])
#reversion.register(ActivityType)
#reversion.register(ActivityCategory, follow=['activities'])
#reversion.register(Activity, follow=['park_set', 'zone_set', 'trail_set', 'requireddocument_set', 'proposalparkactivity_set','proposalparkzoneactivity_set', 'proposaltrailsectionactivity_set'])
#reversion.register(Park, follow=['zones', 'requireddocument_set', 'proposals'])
#reversion.register(Zone, follow=['proposal_zones'])
#reversion.register(Trail, follow=['sections', 'proposals'])
#reversion.register(Section, follow=['proposal_trails'])
#reversion.register(RequiredDocument)
#reversion.register(ApplicationType, follow=['tenure_app_types', 'helppage_set'])
#reversion.register(ActivityMatrix)
#reversion.register(Tenure)
#reversion.register(Question)
reversion.register(UserAction)
reversion.register(CommunicationsLogEntry)
reversion.register(Document)
reversion.register(SystemMaintenance)

