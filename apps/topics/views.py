from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.topics.serializers import ListTopicsSerializer
from apps.topics.models import Topics


class TopicsListView(ListAPIView):
    queryset = Topics.objects.all()
    serializer_class = ListTopicsSerializer
    permission_classes = [AllowAny]
