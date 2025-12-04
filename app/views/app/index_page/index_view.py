import logging

from django.http import HttpRequest
from django.shortcuts import render

from app.views.app.contexts.index_context import IndexContextManager

logger = logging.getLogger("app.views")


# ===================== View =====================

def index_page_view(request: HttpRequest):
    """Главная страница App"""
    context = IndexContextManager(request).get()
    # logger.info(msg=f"Context Index Page: {context}")

    return render(request, template_name='app/site/pages/index/index-wrapp.dj.html', context=context)

