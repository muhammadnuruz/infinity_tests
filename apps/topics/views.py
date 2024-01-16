from rest_framework import generics
from rest_framework.generics import ListAPIView
from apps.topics.serializers import ListTopicsSerializer
from apps.topics.models import Topics
from apps.users.permissions import UserPermission


class TopicsListView(ListAPIView):
    queryset = Topics.objects.all()
    serializer_class = ListTopicsSerializer
    permission_classes = [UserPermission]
