from django.conf import settings
from django.core.mail import send_mail


def send_email_notification(user, subject, message):
    try:
        if user.email:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
    except Exception as e:  # pylint: disable=broad-except
        print(f"Failed to send mail. {e}")
