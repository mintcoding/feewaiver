import os
from io import BytesIO

from django.conf import settings
from docxtpl import DocxTemplate
from feewaiver.main_models import GlobalSettings


#def create_apiary_licence_pdf_contents(approval, proposal, copied_to_permit, approver, site_transfer_preview=None):
def create_feewaiver_pdf_contents(feewaiver):

    feewaiver_template = GlobalSettings.objects.get(key=GlobalSettings.KEY_FEEWAIVER_TEMPLATE_FILE)

    if feewaiver_template._file:
        path_to_template = feewaiver_template._file.path
    else:
        # Use default template file
        path_to_template = os.path.join(settings.BASE_DIR, 'feewaiver', 'static', 'feewaiver', 'fee_waiver_template.docx')

    doc = DocxTemplate(path_to_template)
    #from disturbance.components.approvals.serializers import ApprovalSerializerForLicenceDoc
    from feewaiver.serializers import FeeWaiverSerializer
    serializer_context = {
            }
    context_obj = FeeWaiverSerializer(feewaiver, context=serializer_context)
    context = context_obj.data
    doc.render(context)

    temp_directory = settings.BASE_DIR + "/tmp/"
    try:
        os.stat(temp_directory)
    except:
        os.mkdir(temp_directory)

    f_name = temp_directory + 'feewaiver_' + str(feewaiver.id)
    new_doc_file = f_name + '.docx'
    new_pdf_file = f_name + '.pdf'
    doc.save(new_doc_file)
    os.system("libreoffice --headless --convert-to pdf " + new_doc_file + " --outdir " + temp_directory)

    file_contents = None
    with open(new_pdf_file, 'rb') as f:
        file_contents = f.read()
    os.remove(new_doc_file)
    os.remove(new_pdf_file)
    return file_contents
