from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from app.views.app.contexts.bsae_context import BaseContextManager


def terms_page_view(request: HttpRequest) -> HttpResponse:
    context = BaseContextManager(request).get()
    return render(
        request,
        template_name='app/site/pages/terms/terms_wrapp.dj.html',
        context=context,
    )

