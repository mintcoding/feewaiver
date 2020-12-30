import logging
import mimetypes

import six
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.core.urlresolvers import reverse
from django.template import loader, Template#, Context
from django.utils.html import strip_tags
from ledger.accounts.models import Document
from django.utils.encoding import smart_text
from django.core.urlresolvers import reverse
from feewaiver.models import AssessorsGroup, ApproversGroup
#from disturbance.components.emails.emails import TemplateEmailBase
from ledger.accounts.models import EmailUser
import os
logger = logging.getLogger('log')
#logger = logging.getLogger(__name__)

SYSTEM_NAME = settings.SYSTEM_NAME_SHORT + ' Automated Message'


def _render(template, context):
    if isinstance(context, dict):
        pass
        #context = Context(context)
        #context.update({'settings': settings})
    if isinstance(template, six.string_types):
        template = Template(template)
    return template.render(context)

def prepare_attachments(attachments):
    returned_attachments = []
    for document in attachments.all():
        path, filename = os.path.split(document._file.name)    
        returned_attachments.append(
            (filename, document._file.read())
        )
    return returned_attachments


def host_reverse(name, args=None, kwargs=None):
    return "{}{}".format(settings.DEFAULT_HOST, reverse(name, args=args, kwargs=kwargs))


class TemplateEmailBase(object):
    subject = ''
    #html_template = 'feewaiver/feewaiver/templates/feewaiver/emails/base_email.html'
    # txt_template can be None, in this case a 'tag-stripped' version of the html will be sent. (see send)
    #txt_template = 'feewaiver/feewaiver/templates/feewaiver/emails/base_email.txt'

    def send_to_user(self, user, context=None):
        return self.send(user.email, context=context)

    def send(self, to_addresses, from_address=None, context=None, attachments=None, cc=None, bcc=None):
        #import ipdb; ipdb.set_trace()
        """
        Send an email using EmailMultiAlternatives with text and html.
        :param to_addresses: a string or a list of addresses
        :param from_address: if None the settings.DEFAULT_FROM_EMAIL is used
        :param context: a dictionary or a Context object used for rendering the templates.
        :param attachments: a list of (filepath, content, mimetype) triples
               (see https://docs.djangoproject.com/en/1.9/topics/email/)
               or Documents
        :param bcc:
        :param cc:
        :return:
        """
        # The next line will throw a TemplateDoesNotExist if html template cannot be found
        html_template = loader.get_template(self.html_template)
        # render html
        html_body = _render(html_template, context)
        if self.txt_template is not None:
            txt_template = loader.get_template(self.txt_template)
            txt_body = _render(txt_template, context)
        else:
            txt_body = strip_tags(html_body)

        # build message
        if isinstance(to_addresses, six.string_types):
            to_addresses = [to_addresses]
        if attachments is None:
            attachments = []
        if attachments is not None and not isinstance(attachments, list):
            attachments = list(attachments)

        if attachments is None:
            attachments = []

        # Convert Documents to (filename, content, mime) attachment
        _attachments = []
        for attachment in attachments:
            if isinstance(attachment, Document):
                filename = str(attachment)
                content = attachment.file.read()
                mime = mimetypes.guess_type(attachment.filename)[0]
                _attachments.append((filename, content, mime))
            else:
                _attachments.append(attachment)
        msg = EmailMultiAlternatives(self.subject, txt_body, from_email=from_address, to=to_addresses,
                                     attachments=_attachments, cc=cc, bcc=bcc)
        msg.attach_alternative(html_body, 'text/html')
        try:
            if not settings.DISABLE_EMAIL:
                msg.send(fail_silently=False)
            logger.info("Email sent to: {} - subject: {}".format(to_addresses, self.subject))
            return msg
        except Exception as e:
            logger.exception("Error while sending email to {}: {}".format(to_addresses, e))
            return None


class FeeWaiverReceivedNotificationEmail(TemplateEmailBase):
    subject = 'Your fee waiver request has been received'
    #html_template = 'feewaiver/emails/proposals/send_referral_notification.html'
    #txt_template = 'feewaiver/emails/proposals/send_referral_notification.txt'
    html_template = 'feewaiver/email/fee_waiver_received_notification.html'
    txt_template = 'feewaiver/email/fee_waiver_received_notification.txt'

class FeeWaiverWorkflowNotificationEmail(TemplateEmailBase):
    subject = 'Fee Waiver request workflow notification'
    #html_template = 'feewaiver/emails/proposals/send_referral_notification.html'
    #txt_template = 'feewaiver/emails/proposals/send_referral_notification.txt'
    html_template = 'feewaiver/email/fee_waiver_workflow_notification.html'
    txt_template = 'feewaiver/email/fee_waiver_workflow_notification.txt'

class FeeWaiverApproverNotificationEmail(TemplateEmailBase):
    subject = 'Fee Waiver request approver notification'
    #html_template = 'feewaiver/emails/proposals/send_referral_notification.html'
    #txt_template = 'feewaiver/emails/proposals/send_referral_notification.txt'
    html_template = 'feewaiver/email/fee_waiver_approver_notification.html'
    txt_template = 'feewaiver/email/fee_waiver_approver_notification.txt'


def send_fee_waiver_received_notification(fee_waiver,request):
    email = FeeWaiverReceivedNotificationEmail()
    #url = request.build_absolute_uri(reverse('internal-referral-detail',kwargs={'proposal_pk':referral.proposal.id,'referral_pk':referral.id}))

    context = {
        'feewaiver': fee_waiver
    }

    #def send(self, to_addresses, from_address=None, context=None, attachments=None, cc=None, bcc=None):
    msg = email.send(fee_waiver.contact_details.email, context=context)
    #sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    # should always be noreply@dbca.wa.gov.au
    sender = settings.DEFAULT_FROM_EMAIL
    #msg = email.send(fee_waiver.contact_details.email, context=context)
    _log_feewaiver_email(msg, fee_waiver, sender=sender)

def send_workflow_notification(fee_waiver,request, action, email_subject=None, workflow_entry=None):
    email = FeeWaiverWorkflowNotificationEmail()
    if email_subject:
        email.subject = email_subject
    url = request.build_absolute_uri(reverse('internal-feewaiver-detail',kwargs={'feewaiver_pk':fee_waiver.id}))

    comments = request.data.get('comments')
    context = {
        'feewaiver': fee_waiver,
        'comments': comments,
        'url': url,
    }

    #def send(self, to_addresses, from_address=None, context=None, attachments=None, cc=None, bcc=None):
    #to_addresses = fee_waiver.assigned_officer.email
    if action in ["propose_issue", "propose_concession", "propose_decline"]:
        to_addresses = list(ApproversGroup.objects.first().members.all().values_list('email', flat=True))
    if action in ["return_to_assessor", "submit"]:
        to_addresses = list(AssessorsGroup.objects.first().members.all().values_list('email', flat=True))
    if action in ["issue", "issue_concession", "decline"]:
        to_addresses = fee_waiver.contact_details.email
    #sender = request.user if request else settings.DEFAULT_FROM_EMAIL
    # should always be noreply@dbca.wa.gov.au
    sender = settings.DEFAULT_FROM_EMAIL
    if workflow_entry:
        msg = email.send(to_addresses, sender, context=context, attachments=prepare_attachments(workflow_entry.documents))
        _log_feewaiver_email(msg, fee_waiver, sender=sender, workflow_entry=workflow_entry)
    else:
        msg = email.send(to_addresses, sender, context=context)
        _log_feewaiver_email(msg, fee_waiver, sender=sender)
    #msg = email.send(fee_waiver.contact_details.email, context=context)
    #if referral.proposal.applicant:
     #   _log_org_email(msg, referral.proposal.applicant, referral.referral, sender=sender)

def send_approver_notification(fee_waiver,request, action):
    email = FeeWaiverApproverNotificationEmail()
    #if email_subject:
     #   email.subject = email_subject

    #comments = request.data.get('comments')
    context = {
        'feewaiver': fee_waiver,
        #'comments': comments,
    }
    #if action in ["issue", "issue_concession", "decline"]:
    to_addresses = fee_waiver.contact_details.email
    sender = settings.DEFAULT_FROM_EMAIL
    msg = email.send(to_addresses, sender, context=context, attachments=prepare_attachments(fee_waiver.documents))
    _log_feewaiver_email(msg, fee_waiver, sender=sender)



def _log_feewaiver_email(email_message, fee_waiver, sender=None, workflow_entry=None):
    from feewaiver.models import FeeWaiverLogEntry
    if isinstance(email_message, (EmailMultiAlternatives, EmailMessage,)):
        # TODO this will log the plain text body, should we log the html instead
        text = email_message.body
        subject = email_message.subject
        fromm = smart_text(sender) if sender else smart_text(email_message.from_email)
        # the to email is normally a list
        if isinstance(email_message.to, list):
            to = ','.join(email_message.to)
        else:
            to = smart_text(email_message.to)
        # we log the cc and bcc in the same cc field of the log entry as a ',' comma separated string
        all_ccs = []
        if email_message.cc:
            all_ccs += list(email_message.cc)
        if email_message.bcc:
            all_ccs += list(email_message.bcc)
        all_ccs = ','.join(all_ccs)

    else:
        text = smart_text(email_message)
        subject = ''
        #to = proposal.applicant.email if proposal.applicant.email else ''
        to = fee_waiver.contact_details.email
        fromm = smart_text(sender) if sender else SYSTEM_NAME
        all_ccs = ''

    #customer = referral.referral

    #staff = sender

    kwargs = {
        'subject': subject,
        'text': text,
        'fee_waiver': fee_waiver,
        #'proposal': referral.proposal,
        #'customer': customer,
        #'staff': staff,
        'to': to,
        'fromm': fromm,
        'cc': all_ccs
    }

    if not workflow_entry:
        email_entry = FeeWaiverLogEntry.objects.create(**kwargs)
    else:
        email_entry = FeeWaiverLogEntry.objects.update_or_create(id=workflow_entry.id, defaults=kwargs)
        #email_entry = workflow_entry.save(**kwargs)

    return email_entry

