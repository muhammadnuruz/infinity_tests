from django.urls import path

from apps.categories.views import CategoriesDetailViewSet, CategoriesListViewSet

urlpatterns = [
    path('', CategoriesListViewSet.as_view(),
         name='categories-list'),
    path('detail/<int:pk>/', CategoriesDetailViewSet.as_view(),
         name='categories-detail'),
]
