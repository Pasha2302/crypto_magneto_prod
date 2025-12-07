# app/tasks.py
from celery import shared_task

from app.tasks_all.create_fake_data_coin.fake_data_starter import FakeDataCoinManager
from app.tasks_all.db_monitoring_tasks import save_db_connections_snapshot
# from app.tasks_all.send_contact import send_contact_email


# ===================================================  Crone   =================================================== #

# < queue= > Celery направит задачу в соответствующую очередь,
# и её подхватит только воркер, слушающий именно эту очередь.
@shared_task(queue='default')
def start_every_10_minutes():
    """ Каждые 10 минут """
    save_db_connections_snapshot()

@shared_task(queue='default')
def start_every_one_hours():
    """ Каждый час """
    FakeDataCoinManager().run()

@shared_task(queue='default')
def start_every_two_hours():
    """ Каждые два часа """
    pass

# ================================================== No Crone  ==================================================== #

# @shared_task
# def generate_video_frame_task(model_label: str, object_id: int, at_second: int = 15):
#     """ Celery задача для генерации кадра видео. """
#     # from app.db_models.actress_models.actress import ActressVideoFile
#     from django.apps import apps
#
#     model_class = apps.get_model(model_label)   # получаем класс модели
#     video_obj = model_class.objects.get(pk=object_id)
#     generate_video_frame(video_obj, at_second=at_second)

