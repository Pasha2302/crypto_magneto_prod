# !!! Важно проимортировать сигнады в apps.py
import os

from django.db.models import FileField
from django.db.models.signals import pre_save, post_delete

from app.db_models import Coin
from app.db_models.site_models import ImageSite, ImageSocial

import logging
logger = logging.getLogger("app.signals")


# =================================================================================================================== #
# =============================== Функции удаления файлов ======================================================== #
# =================================================================================================================== #

def delete_file(path):
    """Удалить файл с диска, если он существует"""
    logger.info(f"\n[INFO] Deleting File:\n{path}\n{'--' * 40}")
    if path and os.path.isfile(path):
        os.remove(path)


def auto_delete_files_on_delete(sender, instance, **kwargs):
    """Удаляем все файлы при удалении объекта"""
    for field in sender._meta.get_fields():
        if isinstance(field, FileField):
            file = getattr(instance, field.name, None)
            if file and hasattr(file, "path"):
                delete_file(file.path)


def auto_delete_files_on_change(sender, instance, **kwargs):
    """
    Автоматически удаляет старые файлы с диска при обновлении записи модели.
    Особенности:
    - Для всех FileField/ ImageField проверяется,
      был ли файл заменён, и старый файл удаляется.

    Параметры:
    ----------
    sender : Type[models.Model]
        Класс модели, для которого сработал сигнал.
        Например: ActressImage, ActressVideoFile, Actress.
    instance : models.Model
        Экземпляр модели, который сохраняется (новые данные ещё в базе нет).
        Например:
            instance.image -> <FieldFile: actresses/actress_page-slug/videos/frame.jpg>
    **kwargs : dict
        Дополнительные параметры сигнала Django (обычно не используются).
        Содержат ключи: 'raw', 'using', 'update_fields', и др.

    Пример использования:
    --------------------
    from app.models import ImageSite
    from app.signals import auto_delete_files_on_change

    # Предположим, что сигнал зарегистрирован через:
    pre_save.connect(auto_delete_files_on_change, sender=ImageSite)

    # Когда мы обновляем видео:
    obj_img = ImageSite.objects.get(pk=1)
    obj_img.image = new_file  # старый файл удалится автоматически
    obj_img.save()  # вызов сигнала pre_save -> старый video_file и title_frame удаляются

    """
    if not instance.pk:
        # Новый объект, нечего удалять
        return
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # Объект неожиданно не найден — пропускаем
        return

    # ===== Удаление файлов =====
    for field in sender._meta.get_fields():
        if isinstance(field, FileField):
            old_file = getattr(old_instance, field.name, None)
            new_file = getattr(instance, field.name, None)
            if old_file and old_file != new_file and hasattr(old_file, "path"):
                delete_file(old_file.path)

# =================================================================================================================== #
# =============================== Регистрация сигналов ============================================================ #
# =================================================================================================================== #

def register_file_cleanup():
    """
        Регистрация сигналов для конкретной модели.
        Вызываем в apps.py
        Импорт сигналов в ready() — правильный способ, чтобы сигналы не подключались дважды.
    """
    # Подключаем авто-удаление только к выбранным моделям
    for model in (ImageSite, Coin, ImageSocial, ):  # StripperVideo
        post_delete.connect(auto_delete_files_on_delete, sender=model)
        pre_save.connect(auto_delete_files_on_change, sender=model)

