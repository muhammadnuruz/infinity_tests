from django.urls import path, include

urlpatterns = [
    path('', include("apps.core.urls")),
    path('users/', include("apps.users.urls")),
    path('topics/', include("apps.topics.urls")),
    path('tests/', include("apps.tests.urls")),
]
