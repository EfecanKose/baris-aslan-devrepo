from django.db.models.signals import  post_save
from django.dispatch import receiver
from support.models import AdminMessage
from django.core.mail import send_mail



@receiver(post_save, sender=AdminMessage)
def send_mail_customer(sender, instance, **kwargs):

    send_mail(
        instance.support.subject,
        instance.message,
        'gonderen@example.com',
        [instance.support.email],
        fail_silently=False,
    )