import logging

from django.http import HttpRequest
from django.shortcuts import render

from app.views.app.contexts.bsae_context import BaseContextManager


logger = logging.getLogger("app.views")


def contact_page_view(request: HttpRequest):
    """Главная страница App"""
    logger.info(msg=f"Obj Request: {request}")
    context = BaseContextManager(request, name_page='contact').get()

    return render(request, template_name='app/site/pages/contact/contact_wrapp.dj.html', context=context)

