from django.urls import path

from apps.topics.views import TopicsListView

urlpatterns = [
    path('', TopicsListView.as_view(), name='topic-list')
]
