from django.utils.translation import activate, gettext_lazy as _
from rest_framework import serializers

from userauth.models import CustomUser
from .models import Notification, NotificationTypes


class NotificationBaseSerializer(serializers.ModelSerializer):
    notification_type = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        exclude = ("user",)

    def get_notification_type(self, obj):
        activate('ru')
        return _(NotificationTypes(obj.notification_type).label)

class NotificationTypesSerializer(serializers.Serializer):
    code = serializers.CharField()
    label = serializers.CharField()

    def to_representation(self, instance):
        return {
            'value': instance,
            'name': dict(NotificationTypes.choices).get(instance)
        }


class NotificationCreateSerializer(NotificationBaseSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=True,
        error_messages={'required': 'User ID required.'}
    )
    notification_type = serializers.ChoiceField(
        choices=NotificationTypes.choices,
        required=True,
        error_messages={
            'required': 'Choose notification type.',
            'invalid_choice': 'Invalid notification type.',
        }
    )

    class Meta:
        model = Notification
        fields = ['user', 'title', 'body', 'html', 'notification_type']
        extra_kwargs = {
            'title': {'required': True, 'error_messages': {'required': 'Title is required.'}},
            'body': {'required': False},
            'html': {'required': False}
        }
