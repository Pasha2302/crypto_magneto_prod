from celery import shared_task
from django.core.mail import EmailMultiAlternatives


@shared_task
def send_contact_email(subject, text_body, html_body, user_email):
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        # Если в EmailMultiAlternatives не указан from_email,
        # Django берёт значение по умолчанию из settings.DEFAULT_FROM_EMAIL
        from_email=None,
        to=["info@cryptogugu.com"],  # письмо придёт на этот адрес
        # to = ["info@cryptogugu.com", "someone@another.com"] # несколько адресов
        reply_to=[user_email],   # Добавить возможность ответить сразу пользователю (появляется кнопка)
    )
    msg.attach_alternative(html_body, "text/html")
    msg.send()


@shared_task
def message_to_user(user_email):
    # Сообщение пользователю (опционально) — автоответ
    auto = EmailMultiAlternatives(
        subject="We received your request",
        body="Thanks! We will contact you soon.",
        from_email=None,
        to=[user_email],
    )
    auto.send()