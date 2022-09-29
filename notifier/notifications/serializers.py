import datetime

from rest_framework import serializers
from notifications import models


class BulkNotificationSerializer(serializers.ModelSerializer):

    def _validate_start_end(self, attrs):
        start = attrs.get('start')
        end = attrs.get('end')
        if self.instance:
            start = start or self.instance.start
            end = end or self.instance.end

        if start >= end:
            raise serializers.ValidationError('Start date must be less than end date.')

    def validate(self, attrs):
        self._validate_start_end(attrs)
        return attrs

    class Meta:
        model = models.BulkNotification
        fields = ('message', 'start', 'end', 'filter')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Client
        fields = ('number', 'code', 'tag', 'timezone')
