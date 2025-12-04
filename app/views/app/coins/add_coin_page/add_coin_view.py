from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from app.views.app.contexts.bsae_context import BaseContextManager


def disclaimer_page_view(request: HttpRequest) -> HttpResponse:
    context = BaseContextManager(request).get()
    return render(
        request,
        template_name='app/site/pages/disclaimer/disclaimer_wrapp.dj.html',
        context=context,
    )

