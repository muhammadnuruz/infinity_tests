from django.urls import path, include

urlpatterns = [
    path('', include("apps.core.urls")),
    path('tests/', include("apps.tests.urls")),
    path('telegram-users/', include("apps.telegram_users.urls")),
]
