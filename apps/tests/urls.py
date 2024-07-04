from django.urls import path
from .views import GetTestView, SubmitAnswerView, EndTestView

urlpatterns = [
    path('get-test/<str:chat_id>/', GetTestView.as_view(), name='get-test'),
    path('submit-answer/<str:chat_id>/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('end-test/<str:chat_id>/', EndTestView.as_view(), name='end-test'),
]
