from app.db_models.site_models import ImageSite


def admin_global_data(request):
    """
        Добавляет глобальный объект для админки.
        Будет доступен в любом шаблоне админки через
        Для работы нужно добавить в settings.py :
        TEMPLATES = [
            ......
            'OPTIONS': {
                ......
                'context_processors': [..., 'app.admin_registration.base_context.context_processors.admin_global_data',]
            }
        ]
    """
    if request.path.startswith('/admin/'):  # или '/logginaizerrs/' если у тебя кастомный админ путь
        obj_admin_img = {
            obj_img.name: obj_img
            for obj_img in ImageSite.objects.filter(name_page='admin')
            if obj_img.image
        }
        return {
            'obj_admin_img': obj_admin_img,
        }
    return {}
