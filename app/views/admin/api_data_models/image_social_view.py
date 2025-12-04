from django.http import HttpRequest, JsonResponse

from app.db_models import ImageSocial


def get_image_social_view(request: HttpRequest):
    if request.method == "POST":
        return JsonResponse(data={'error': 'Method Not Allowed' }, status=405)

    data = {obj.pk: obj.img_64.url for obj in ImageSocial.objects.all() if obj.image}

    return JsonResponse({"data": data}, status=200)
