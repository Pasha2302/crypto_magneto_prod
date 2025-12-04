from django.urls import path, include


urlpatterns = [
    path('', include('app.views.urls_app')),          # обычные ручки
    path('admin-api/', include('app.views.urls_admin')),  # админские ручки
    path('api-app-v1/', include('app.views.urls_api_app')),  # api app ручки
]

