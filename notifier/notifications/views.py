from rest_framework import generics
from rest_framework.response import Response

from notifications import models
from notifications import serializers
from notifications.models import NotificationStatus


class BulkNotificationView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.BulkNotification.objects.all()
    serializer_class = serializers.BulkNotificationSerializer


class BulkNotificationViewList(generics.ListCreateAPIView):
    queryset = models.BulkNotification.objects.all()
    serializer_class = serializers.BulkNotificationSerializer


class ClientView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer


class ClientViewList(generics.ListCreateAPIView):
    queryset = models.Client.objects.all()
    serializer_class = serializers.ClientSerializer


class StatView(generics.RetrieveAPIView):
    queryset = models.BulkNotification.objects.all()
    serializer_class = serializers.BulkNotificationSerializer

    def get(self, request, *args, **kwargs):
        # TODO dirty
        instance = self.get_object()
        return Response({
            'id': instance.pk,
            'message': instance.message,
            'stats': {
                'success': instance.notification_set.filter(status=NotificationStatus.success).count(),
                'error': instance.notification_set.filter(status=NotificationStatus.error).count(),
                'daft': instance.notification_set.filter(status=NotificationStatus.draft).count()
            }
        })
