from post.models import Post, Notification
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
@receiver(post_save, sender=Post)
def create_notification(sender, instance, created, **kwargs):
    if created:
        message = instance.content[:30]
        notification = Notification.objects.create(
            user=instance.user,
            message=message,
        )



