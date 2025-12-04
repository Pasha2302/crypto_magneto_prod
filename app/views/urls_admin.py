from django.urls import path

from app.views.admin.api_data_models.image_social_view import get_image_social_view

# admin-api/get-image-social/
urlpatterns = [
    path(route='get-image-social/', view=get_image_social_view, name='get_image_social_view'),

]