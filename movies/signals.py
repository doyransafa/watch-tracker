from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Follow
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



@receiver(post_save, sender=Follow)
def follow_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        group_name = instance.following.notification_group_name
        event = {
            'type' : 'user_followed',
            'username' : instance.follower.username
        }
        async_to_sync(channel_layer.group_send)(group_name, event)