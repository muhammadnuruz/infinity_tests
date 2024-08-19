from django.urls import path

from apps.words.views import WordsDetailViewSet, WordsUpdateViewSet, WordsCreateViewSet, WordsListViewSet

urlpatterns = [
    path('', WordsListViewSet.as_view(),
         name='words-list'),
    path('create/', WordsCreateViewSet.as_view(),
         name='words-create'),
    path('detail/<int:pk>/', WordsDetailViewSet.as_view(),
         name='words-detail'),
    path('update/<int:pk>/', WordsUpdateViewSet.as_view(),
         name='words-update')
]
