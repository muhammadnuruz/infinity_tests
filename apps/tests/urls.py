from django.urls import path

from apps.tests.views import GetTestView, SubmitAnswerView, EndTestView

urlpatterns = [
    path('get_test/<int:topic_id>/', GetTestView.as_view(), name='get-test'),
    path('submit_anser/', SubmitAnswerView.as_view(), name='submit-answer'),
    path('end_test/', EndTestView.as_view(), name='end-test')
]
