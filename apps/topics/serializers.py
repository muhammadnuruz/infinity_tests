from apps.topics.models import Topics
from rest_framework import serializers


class ListTopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['id', 'name']
