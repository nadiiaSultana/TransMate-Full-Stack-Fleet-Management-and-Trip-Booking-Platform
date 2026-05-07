from django.core.mail import send_mail
from django.conf import settings

def send_transmate_email(to_email, subject, message):
    if not to_email: return False
    send_mail(subject=subject, message=message, from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[to_email], fail_silently=False)
    return True
