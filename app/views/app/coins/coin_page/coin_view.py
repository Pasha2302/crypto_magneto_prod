from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from app.db_models import Coin, Label
from app.views.app.contexts.bsae_context import BaseContextManager
from app.views.app.contexts.coin_context.tools import (
    formatted_launch_date, render_format_price, format_value_number
)


class CoinPageContextManager:
    def __init__(self, request: HttpRequest, chain_symbol: str, coin_slug: str):
        self.request = request
        self.chain_symbol = chain_symbol
        self.coin_slug = coin_slug

        self.__context = BaseContextManager(self.request, name_page='page_coin').get()

    @staticmethod
    def __set_data_coin(context: dict, chain_symbol: str, coin_slug: str):
        label_prefetch = Prefetch(
            'labels',
            queryset=Label.objects.all(),
            to_attr='labels_coin'
        )

        coin_obj = get_object_or_404(
            Coin.objects.select_related("chain").prefetch_related(label_prefetch),
            chain__symbol__iexact=chain_symbol,  # без учёта регистра
            slug=coin_slug
        )

        coin_obj.launch_date = formatted_launch_date(date_type=coin_obj.launch_date)
        coin_obj.format_price = render_format_price(format_price=coin_obj.format_price)
        coin_obj.symbol = coin_obj.symbol if coin_obj.symbol.startswith('$') else f"${coin_obj.symbol}"
        coin_obj.market_cap = format_value_number(value_int=coin_obj.market_cap)
        coin_obj.volume_usd = format_value_number(value_int=coin_obj.volume_usd)

        # Safety And Audit:
        obj_safety = getattr(coin_obj, 'safety_and_audit', None)
        if obj_safety:
            coin_obj.audit_status = obj_safety.audit_status
            coin_obj.security_score = obj_safety.security_score or 0.0
            coin_obj.audit_provider = obj_safety.audit_provider
            coin_obj.last_date = obj_safety.last_date

        explorer_url = coin_obj.chain.explorer.url
        coin_obj.explorer_url_f = (
            f"{explorer_url}{coin_obj.contract_address}"
            if explorer_url.endswith("/")
            else f"{explorer_url}/{coin_obj.contract_address}"
        )
        coin_obj.socials_qs = coin_obj.socials.all()
        context['coin_obj'] = coin_obj

    def get(self) -> dict:
        self.__set_data_coin(self.__context, self.chain_symbol, self.coin_slug)
        return self.__context


def coin_page_view(request: HttpRequest, chain_symbol, coin_slug) -> HttpResponse:
    context = CoinPageContextManager(request, chain_symbol=chain_symbol, coin_slug=coin_slug).get()
    return render(
        request,
        template_name='app/site/pages/coins/coin/coin_wrapp.html',
        context=context,
    )

