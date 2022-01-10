# encoding: utf-8

from rest_framework import serializers

from api.models import UserRequestHistory


class UserRequestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequestHistory
        #exclude = ['date', 'name', 'symbol', 'open', 'high', 'low', 'close', 'user']
        fields = "__all__"
