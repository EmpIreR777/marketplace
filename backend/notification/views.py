import logging

from django.db import transaction
from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin

from notification.models import Notification, NotificationTypes
from notification.schemas_swagger import notifications_list_schema, notifications_count_schema, \
    notifications_create_schema, notifications_get_types_schema, notifications_mark_all_as_read_schema, \
    notifications_mark_read_by_id_schema
from notification.serializers import (
    NotificationBaseSerializer,
    NotificationCreateSerializer,
    NotificationTypesSerializer,
)
from notification.services import send_notification_count


logger = logging.getLogger(__name__)


class NotificationViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Notification.objects.all()

    def get_serializer_class(self):
        """Get serializer class based on url"""
        if self.action == 'list':
            return NotificationBaseSerializer
        elif self.action == 'create_notification':
            return NotificationCreateSerializer
        elif self.action == 'get_notification_types':
            return NotificationTypesSerializer
        return NotificationBaseSerializer

    def get_permissions(self):
        """Display notification only to authenticated users."""
        if self.action == 'create_notification' or self.action == 'get_notification_types':
            return [IsAdminUser()]
        else:
            return [IsAuthenticated()]

    def get_queryset(self):
        """Return notifications for user"""
        return super().get_queryset().filter(user=self.request.user)

    @notifications_list_schema
    def list(self, request, *args, **kwargs):
        """Return paginated notifications list"""
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='get_notification_types')
    @notifications_get_types_schema
    def get_notification_types(self, request):
        """Return notification types"""
        notification_types = NotificationTypes.choices
        data = [{'code': code, 'label': label} for code, label in notification_types]
        return Response(data)

    @action(detail=False, methods=['post'], url_path='create_notification')
    @notifications_create_schema
    def create_notification(self, request):
        """Create new notification"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        title = serializer.validated_data.get('title')
        body = serializer.validated_data.get('body')
        html = serializer.validated_data.get('html')
        notification_type = serializer.validated_data.get('notification_type')
        try:
            Notification.objects.create(
                user=user,
                title=title,
                body=body,
                html=html,
                notification_type=notification_type,
            )
            send_notification_count(user)
        except Exception:
            raise APIException("Failed to create notification")
        return HttpResponse(status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['patch'], url_path='mark_notification_read')
    @notifications_mark_read_by_id_schema
    def mark_notification_read(self, request, pk):
        """Mark notification as read."""
        try:
            notification = Notification.objects.get(id=pk)
        except Notification.DoesNotExist:
            raise APIException('Notification not found')
        if not notification.is_read:
            notification.is_read = True
            notification.save()
            send_notification_count(request.user)
        return Response(status=status.HTTP_200_OK, data={"is_success": True})

    @action(methods=["post"], detail=False)
    @notifications_mark_all_as_read_schema
    @transaction.atomic
    def mark_all_as_read(self, request):
        """Marks all unread notification as read."""
        user = request.user
        updated = self.get_queryset().filter(user=user, is_read=False).update(is_read=True)
        send_notification_count(request.user)
        return Response(status=status.HTTP_200_OK,
                        data={"status": f"marked {updated} notifications as read", "is_success": True})

    @notifications_count_schema
    @action(methods=["get"], detail=False)
    def count(self, request):
        """Returns the number of notifications."""
        send_notification_count(request.user)
        return Response({"count": self.get_queryset().filter(is_read=False).count()})
