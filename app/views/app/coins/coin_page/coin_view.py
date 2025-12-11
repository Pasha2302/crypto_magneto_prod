import random
from datetime import datetime, timedelta
from decimal import Decimal

from django.utils import timezone
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404

from app.db_models import Coin, Label
from app.views.app.contexts.bsae_context import BaseContextManager
from app.views.app.contexts.coin_context.tools import (
    formatted_launch_date, render_format_price, format_value_number, format_float
)
from django.core.cache import cache
import logfire


def generate_daily_history(base_price: Decimal, years: int = 4):
    """Генерирует исторические OHLC + value."""

    base_price = round(base_price, 9)
    if base_price == 0:
        return []

    days = years * 365
    today = timezone.now().date()

    result = []
    price = base_price

    # ограничения колебаний
    max_daily_change = Decimal("0.06")   # максимум 6% диапазона
    min_daily_change = Decimal("0.01")   # минимум 1%

    for i in range(days + 1):
        date = today - timedelta(days=i)

        if i == 0:
            # первая свеча — фиксируем open = close = base_price
            open_price = price
            close_price = price
            high_price = price
            low_price = price
        else:
            # --------- 1) Генерируем изменение цены ---------
            direction = 1 if random.random() > 0.5 else -1
            percent = Decimal(str(random.uniform(float(min_daily_change),
                                                 float(max_daily_change))))
            close_price = price - price * percent * direction
            close_price = round(close_price, 9)

            # --------- 2) Свеча OHLC ---------
            open_price = price

            # волатильность внутри дня
            intraday_vol = float(percent) * float(price)

            high_price = float(open_price) + random.uniform(0, intraday_vol)
            low_price = float(open_price) - random.uniform(0, intraday_vol)

            # high >= max(open, close)
            high_price = max(high_price, float(open_price), float(close_price))
            # low <= min(open, close)
            low_price = min(low_price, float(open_price), float(close_price))

            # округления
            open_price = round(float(open_price), 9)
            high_price = round(high_price, 9)
            low_price = round(low_price, 9)
            close_price = round(float(close_price), 9)

            # новая база для следующей свечи
            price = Decimal(str(close_price))

        result.append({
            "time": date.isoformat(),
            "open": open_price,
            "high": high_price,
            "low": low_price,
            "close": close_price,
            "value": close_price  # для текущего line-графика
        })

    result.reverse()
    return result


def aggregate_weekly(data):
    """Берёт последнее значение каждой недели."""
    weekly = {}
    for item in data:
        date = datetime.fromisoformat(item["time"]).date()
        year, week, _ = date.isocalendar()
        weekly[(year, week)] = item  # последнее значение недели

    return list(weekly.values())


def aggregate_monthly(data):
    """Берёт последнее значение каждого месяца."""
    monthly = {}
    for item in data:
        date = datetime.fromisoformat(item["time"]).date()
        key = (date.year, date.month)
        monthly[key] = item

    return list(monthly.values())


def aggregate_yearly(data):
    """Берёт последнее значение каждого года."""
    yearly = {}
    for item in data:
        date = datetime.fromisoformat(item["time"]).date()
        yearly[date.year] = item

    return list(yearly.values())

# ============================================================================================== #

def get_tokenomics_data(coin_obj: Coin) -> dict:
    """
        Формирует данные токеномики для круговой диаграммы.
        Использует circulating_supply, total_supply и max_supply.
    """

    circulating = coin_obj.circulating_supply or 0
    total = coin_obj.total_supply or circulating
    max_supply = coin_obj.max_supply or total

    # 1) В обращении
    circulating_part = circulating

    # 2) Заблокировано / не в обращении
    locked_part = max(total - circulating, 0)

    # 3) Не выпущено
    not_minted_part = max(max_supply - total, 0)

    labels = []
    values = []

    if circulating_part > 0:
        labels.append("Circulating Supply")
        values.append(circulating_part)

    if locked_part > 0:
        labels.append("Locked / Reserved")
        values.append(locked_part)

    if not_minted_part > 0:
        labels.append("Not Yet Minted")
        values.append(not_minted_part)

    return {
        "labels": labels,
        "values": values,
        "max_supply": max_supply,
    }



class CoinPageContextManager:
    def __init__(self, request: HttpRequest, chain_symbol: str, coin_slug: str):
        self.request = request
        self.chain_symbol = chain_symbol
        self.coin_slug = coin_slug

        self.__context = BaseContextManager(self.request, name_page='page_coin').get()

    @staticmethod
    def __get_data_chart_price(current_price: Decimal, coin_id):
        cache_key = f"coin_{coin_id}_chart_price"
        cache_ttl = 600  # время жизни кеша в секундах (например, 10 минут)
        # Попытка получить из кеша
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            logfire.info("Кэш-попадание для get_data_chart_price")
            return cached_result

        # 1) Генерим день за 4 года
        day_data = generate_daily_history(current_price, years=4)
        # 2) Агрегации
        week_data = aggregate_weekly(day_data)
        month_data = aggregate_monthly(day_data)
        year_data = aggregate_yearly(day_data)

        data = {
            "dayData": day_data,
            "weekData": week_data,
            "monthData": month_data,
            "yearData": year_data,
        }
        # Сохраняем результат в кеш
        cache.set(cache_key, data, cache_ttl)
        logfire.info("Кэш установлен для get_data_chart_price", ttl=cache_ttl)

        return data

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
        coin_obj.symbol = coin_obj.symbol if coin_obj.symbol.startswith('$') else f"${coin_obj.symbol}"

        # Метрики рынка:
        coin_obj.format_price = render_format_price(format_price=coin_obj.format_price)
        coin_obj.launch_price = format_value_number(coin_obj.launch_price)
        coin_obj.high_24h_price = format_value_number(coin_obj.high_24h_price)
        coin_obj.low_24h_price = format_value_number(coin_obj.low_24h_price)
        coin_obj.fdmc = format_value_number(coin_obj.fdmc_computed)

        coin_obj.market_cap = format_value_number(value_int=coin_obj.market_cap)
        coin_obj.volume_usd = format_value_number(value_int=coin_obj.volume_usd)
        coin_obj.liquidity_usd = format_value_number(value_int=coin_obj.liquidity_usd)
        coin_obj.total_supply = format_value_number(value_int=coin_obj.total_supply)
        coin_obj.circulating_supply = format_value_number(value_int=coin_obj.circulating_supply)
        coin_obj.max_supply = format_value_number(value_int=coin_obj.max_supply)

        # Safety And Audit:
        obj_safety = getattr(coin_obj, 'safety_and_audit', None)
        if obj_safety:
            coin_obj.audit_status = obj_safety.audit_status.status
            coin_obj.security_score = obj_safety.security_score or 0.0
            coin_obj.audit_provider = obj_safety.audit_provider.provider
            coin_obj.last_date = obj_safety.last_date

        explorer_url = coin_obj.chain.explorer.url
        coin_obj.explorer_url_f = (
            f"{explorer_url}{coin_obj.contract_address}"
            if explorer_url.endswith("/")
            else f"{explorer_url}/{coin_obj.contract_address}"
        )
        coin_obj.socials_qs = coin_obj.socials.all()
        coin_obj.team_members = coin_obj.team.all()

        coin_obj.predictions_all = []
        if hasattr(coin_obj, 'predictions'):
            for data_predict in coin_obj.predictions.all():
                coin_obj.predictions_all.append({
                    "year": data_predict.year,
                    "min_price": data_predict.min_price.normalize(),
                    "avg_price": data_predict.avg_price.normalize(),
                    "max_price": data_predict.max_price.normalize(),
                    "confidence": data_predict.confidence,
                    "confidence_display": data_predict.get_confidence_display(),
                })

        context['coin_obj'] = coin_obj

    @staticmethod
    def __set_more_coins(context, chain_symbol: str, coin_slug: str):
        qs_more_coins = (
            Coin.objects.filter(
            is_published=True,  chain__symbol__iexact=chain_symbol, price_change_24h__isnull=False)
            .exclude(price_change_24h=0)
            .select_related('chain').only(
                'id', 'chain_id',
                'slug', 'name', 'symbol', 'image', 'format_price', 'price_change_24h',
                'chain__symbol',
            )[:6]
        )
        for obj in qs_more_coins:
            obj.format_price = render_format_price(format_price=obj.format_price)

        context['more_coins'] = qs_more_coins

    @staticmethod
    def __set_meta_tags(context):
        coin_obj: Coin = context['coin_obj']
        meta_tags = context['meta']

        coin_name = coin_obj.name
        coin_symbol = coin_obj.symbol

        meta_tags['title'] = f"{coin_name} ({coin_symbol}) - Chart, Price And Market Cap."
        meta_tags['description'] = f"Track {coin_name} volume, market cap, chart and price."

    @staticmethod
    def __set_pie_chart_data(context):
        coin_obj: Coin = context['coin_obj']

        if hasattr(coin_obj, 'pie_charts') and coin_obj.pie_charts.all().exists():
            print(f"Pie Chart Data: {getattr(coin_obj, 'pie_charts')}")
            labels = []
            values = []
            qs_pie_charts = coin_obj.pie_charts.all()
            for obj in qs_pie_charts:
                labels.append(obj.label.name)
                values.append(obj.value)

            context['pie_chart_data'] = {
                "labels": labels,
                "values": values,
            }

        else: context['pie_chart_data'] = {}


    def get(self) -> dict:
        self.__set_data_coin(self.__context, self.chain_symbol, self.coin_slug)
        self.__set_more_coins(self.__context, self.chain_symbol, self.coin_slug)

        self.__context['chart_price_mocke'] = self.__get_data_chart_price(
            self.__context['coin_obj'].price, self.__context['coin_obj'].pk
        )
        self.__set_pie_chart_data(self.__context)

        self.__set_meta_tags(self.__context)
        return self.__context


def coin_page_view(request: HttpRequest, chain_symbol, coin_slug) -> HttpResponse:
    context = CoinPageContextManager(request, chain_symbol=chain_symbol, coin_slug=coin_slug).get()
    return render(
        request,
        template_name='app/site/pages/coins/coin/coin_wrapp.html',
        context=context,
    )

