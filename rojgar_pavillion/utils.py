import qrcode
from io import BytesIO
from django.core.files import File
from templated_mail.mail import BaseEmailMessage
from django.conf import settings

def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    blob = BytesIO()
    img.save(blob, 'PNG')
    return File(blob, name='qr_code.png')

class RegistrationEmail(BaseEmailMessage):
    template_name = "emails/registration_confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()
        context['registration'] = self.context['registration']
        return context