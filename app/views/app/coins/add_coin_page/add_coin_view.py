from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from app.views.app.contexts.bsae_context import BaseContextManager
from app.views.app.contexts.coin_context.tools import get_used_chains, get_socials_data


class AddCoinContextManager:
    def __init__(self, request: HttpRequest):
        self.request = request
        self.__context = BaseContextManager(request, name_page='add_coin').get()

    def get(self):
        self.__context['used_chains'] = get_used_chains()
        self.__context['socials'] = get_socials_data()
        return self.__context


def add_coin_page_view(request: HttpRequest) -> HttpResponse:
    context = AddCoinContextManager(request).get()
    return render(
        request,
        template_name='app/site/pages/coins/add_coin/add_coin_wrapp.dj.html',
        context=context,
    )

def coin_added_success(request: HttpRequest) -> HttpResponse:
    context = BaseContextManager(request, name_page='add_coin').get()

    return render(
        request,
        template_name='app/site/pages/coins/add_coin/add_coin_success.dj.html',
        context=context,
    )

