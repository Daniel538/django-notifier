from rest_framework import generics

from notifications import models
from notifications import serializers


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
