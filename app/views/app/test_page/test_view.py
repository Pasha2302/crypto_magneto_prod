from django.http import JsonResponse, HttpRequest
from django.shortcuts import render
# from django.template.loader import render_to_string

from app.views.app.contexts.bsae_context import BaseContextManager


class TestContextManager:
    def __init__(self, request):
        self.request = request

    def get(self):
        context = BaseContextManager(self.request, name_page='test').get()

        return context


def test_page_view(request: HttpRequest):
    context = TestContextManager(request).get()
    return render(request, template_name="app/site/test_page/test_wrapp.dj.html", context=context)

