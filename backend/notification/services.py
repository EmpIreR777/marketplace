from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification


def send_notification_count(user):
    channel_layer = get_channel_layer()
    unread_count = Notification.objects.filter(user=user, is_read=False).count()
    print('send_notific',unread_count)
    async_to_sync(channel_layer.group_send)(
        f"notifications_{user.id}",
        {
            "type": "send_notification",
            "unread_count": unread_count
        }
    )