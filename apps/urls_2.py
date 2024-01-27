from django.urls import path

from apps.view import index_page, register_page

urlpatterns = [
    path('', index_page, name='index-page'),
    path('register/', register_page, name='register-page'),
]
