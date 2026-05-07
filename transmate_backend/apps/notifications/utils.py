from .models import Notification
from .email_utils import send_transmate_email

def create_notification(user, title, message, send_email=False):
    n=Notification.objects.create(user=user,title=title,message=message)
    if send_email: send_transmate_email(user.email, title, message)
    return n
