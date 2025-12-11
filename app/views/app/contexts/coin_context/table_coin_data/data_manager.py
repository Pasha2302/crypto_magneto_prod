from datetime import timedelta
from typing import Any

import logfire

from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Prefetch, QuerySet, Case, When, Value, IntegerField
from django.db import connection, reset_queries

from app.db_models import Coin, Label
from app.views.app.contexts.coin_context.table_coin_data.queries.queries_coin_table import (
    TableCoinQueryParams, SortField
)

from django.core.cache import cache

from app.views.app.contexts.coin_context.tools import get_used_chains


class CoinDataManager:
    """
    Менеджер для работы с монетами (Coin) и их метками (Label) с поддержкой пагинации и
    оптимизированной загрузки связанных данных.

    Основные возможности:
    1. Получение всех опубликованных монет с пагинацией.
       - Оптимизировано через select_related для цепочки (chain).
       - Prefetch для связанных меток (labels) выполняется после пагинации для минимизации нагрузки.

    2. Получение всех продвигаемых монет (promoted coins) независимо от пагинации основной таблицы.
       - Также оптимизировано через select_related и prefetch_related.

    3. Вспомогательные методы:
       - log_coin_data: выводит информацию о монетах и их метках в консоль.
       - _create_pagination_data: возвращает словарь с данными для пагинации.
       - __debug_sql: выводит все SQL-запросы, выполненные в текущей сессии Django ORM.

    Особенности реализации:
    - select_related + only ограничивает поля основной и связанных моделей, улучшая производительность JOIN.
    - Prefetch используется для связанных меток, чтобы минимизировать количество запросов к БД.
    - Пагинация реализована через django.core.paginator. Paginator с параметрами по умолчанию: 50 элементов на страницу.
    - Методы построены так, чтобы можно было отдельно получать промо-коины и
        обычные опубликованные монеты, не влияя друг на друга.
    """

    def __init__(self, client_params_table_filter: TableCoinQueryParams):
        self.client_params = client_params_table_filter

    @staticmethod
    def __debug_sql():

        for sql in connection.queries:
            logfire.info(
                "[Page Index] SQL Coin Tables",
                sql=sql.get("sql"),
                time=sql.get("time"),
            )

    @staticmethod
    def log_coin_data(coins_obj: list[Coin]):
        for coin_obj in coins_obj:
            labels_coin = None
            if hasattr(coin_obj, 'labels_coin'):
                labels_coin = [{"name": label.name, "slug": label.slug} for label in coin_obj.labels_coin if label]

            logfire.info(
                f"Name: {coin_obj.name}\n"
                f"Symbol: {coin_obj.symbol}\n"
                f"Contract Address: {coin_obj.contract_address}\n"
                f"Chain: {coin_obj.chain.name} [{coin_obj.chain.symbol}]\n"
                f"Price: {coin_obj.price}\n"
                f"Labels Coin: {labels_coin}\n"
            )

    @staticmethod
    def _create_pagination_data(qs: QuerySet, per_page, current_page_number):
        paginator_obj = Paginator(qs, per_page=per_page)
        page_obj = paginator_obj.get_page(current_page_number)

        return {
            "has_previous": page_obj.has_previous(),
            "has_next": page_obj.has_next(),
            "previous_page_number": page_obj.previous_page_number() if page_obj.has_previous() else None,
            "next_page_number": page_obj.next_page_number() if page_obj.has_next() else None,
            "current_page": page_obj.number,
            "total_pages": paginator_obj.num_pages,
            "page_range": list(
                paginator_obj.get_elided_page_range(number=page_obj.number, on_each_side=2, on_ends=1)
            ),
            "total_items": paginator_obj.count,
            "per_page": per_page,
            "items_start_index": page_obj.start_index(),
            "items_end_index": page_obj.end_index(),
        }, page_obj

    @staticmethod
    def __build_query_select_related(qs: QuerySet) -> QuerySet:
        """
        .only() ограничивает поля только основной модели,
            но если указаны поля через "__", и модель подгружается через select_related(),
            то Django ограничит и поля связанной модели.
        FK-поля (например <chain_id>) обязательно должны быть указаны для корректного JOIN.
            (так как поля для таблицы chain ограничены - 'chain__name', 'chain__symbol',
            если недобавить <chain_id> оно будет считаться не нужным и в момент получения данных будут выполняться
             доп. Запросы, так как это поле нужно для поиска данных в БД)
        """
        return (
            qs.select_related('chain')
            .only(
                'id', 'chain_id',

                'slug', 'name', 'symbol', 'contract_address', 'image',
                'price', 'format_price', 'price_change_24h',
                'market_cap', 'market_cap_presale', 'volume_usd', 'volume_btc', 'published_at',

                'chain__name', 'chain__symbol', 'chain__image',
            )
        )

    @staticmethod
    def __build_query_label_prefetch_related(qs: QuerySet) -> QuerySet:
        label_prefetch = Prefetch(
            'labels',
            queryset=Label.objects.all(),
            to_attr='labels_coin'
        )
        return qs.prefetch_related(label_prefetch)

    @staticmethod
    def __sorting_coins(qs: QuerySet, sort_option: str = 'price', sort: str = 'desc'):

        order_prefix = '-' if sort == 'desc' else ''
        # Сортировка при None-значениях
        if sort_option in {'market_cap', 'price', 'volume_usd', 'price_change_24h', 'launch_date'}:
            qs = qs.annotate(
                sort_priority=Case(
                    When(**{f'{sort_option}__isnull': False}, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField()
                )
            ).order_by('sort_priority', f'{order_prefix}{sort_option}', 'id')

        else:
            qs = qs.order_by(f'{order_prefix}{sort_option}', 'id')

        return qs

    @staticmethod
    def __filter_coins(qs: QuerySet, new, presale, doxxed, audited, chain_slug: str) -> QuerySet:
        if not any([new, presale, doxxed, audited, chain_slug]): return qs

        logfire.info(
            "Datas Filter:",
            new=new,
            presale=presale,
            doxxed=doxxed,
            audited=audited,
            chain_slug=chain_slug,
        )

        if new:
            f_date = timezone.now() - timedelta(days=3)
            qs = qs.filter(published_at__gte=f_date)

        if presale: qs = qs.filter(market_cap_presale=True)
        if doxxed: qs = qs.filter(labels__name="Doxxed")
        if audited: qs = qs.filter(labels__name="Audited")

        # Если у монеты есть обе записи labels (Doxxed, Audited) может быть дубликат в данных qs
        # По этому используем qs.distinct() для удаления дубликатов монет.
        if doxxed or audited: qs = qs.distinct()

        if chain_slug: qs = qs.filter(chain__slug=chain_slug)

        return qs

    # ========================================= GET DATA: ======================================================== #

    def get_filter_and_sorted_data_table(self, only_columns=False):
        cp = self.client_params  # сокращение
        # Колонки сортировки
        def format_column_label(l):
            label = l.replace("_", " ")
            match label:
                case "CHANGE":
                    label = "change 24H"

            print(f"Label: {label}")
            return label

        columns = [
            {
                "value": f.value,
                "label": format_column_label(f.name),
                "active": (cp.sort_field == f),
                "direction": cp.sort_direction.value if cp.sort_field == f else None,
            }
            for f in SortField
        ]
        if only_columns: return {"table_columns": columns}

        # Фильтры
        filters = [
            {
                "name": name,
                "label": name.title(),
                "value": value,
            }
            for name, value in cp.filter_options.model_dump().items()
        ]

        data_filter = {
            "table_columns": columns,
            "table_filters": filters,
            "used_chains": get_used_chains(),
        }
        return data_filter

    def get_per_page_datas(self) -> list[dict[str, Any]]:
        ds = [
            {"value": 10, "active": "selected"},
            {"value": 25, "active": ""},
            {"value": 50, "active": ""},
            {"value": 100, "active": ""},
        ]
        if self.client_params.per_page in {10, 25, 50, 100}:
            for d in ds:
                if self.client_params.per_page == d["value"]: d["active"] = "selected"
                else: d["active"] = ""

        return ds

    def get_coins_tops_tables(self):
        cache_key = "coins_tops_tables"
        cache_ttl = 600  # время жизни кеша в секундах (например, 10 минут)
        # Попытка получить из кеша
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            logfire.info("Кэш-попадание для coins_tops_tables")
            return cached_result

        qs_top_gainers = (
            Coin.objects.filter(is_published=True)
            .filter(price_change_24h__gt=0)
            .order_by('-price_change_24h')[:5]
        )

        qs_trending = (
            Coin.objects.filter(is_published=True)
            .exclude(volume_usd__isnull=True)
            .order_by('-volume_usd')[:5]

        )

        qs_most_viewed = (
            Coin.objects.filter(is_published=True)
            .exclude(views__isnull=True)
            .order_by('-views')[:5]
        )

        result = {
            'trending': list(self.__build_query_select_related(qs_trending)),
            'most_viewed': list(self.__build_query_select_related(qs_most_viewed)),
            'top_gainers': list(self.__build_query_select_related(qs_top_gainers)),
        }

        # Сохраняем результат в кеш
        cache.set(cache_key, result, cache_ttl)
        logfire.info("Кэш установлен для coins_tops_tables", ttl=cache_ttl)

        return result

    def get_promoted_coins(self):
        sort_field = self.client_params.sort_field.value
        sort_direction = self.client_params.sort_direction.value

        cache_key = f"coins_promoted_tables_{sort_field}_{sort_direction}"
        cache_ttl = 600  # время жизни кеша в секундах (например, 10 минут)
        # Попытка получить из кеша
        cached_result = cache.get(cache_key)
        if cached_result is not None:
            logfire.info("Кэш-попадание для coins_promoted_tables")
            return cached_result

        qs_coins_prom = Coin.objects.filter(promoted__isnull=False)
        qs_coins_prom = self.__build_query_select_related(qs=qs_coins_prom)
        qs_coins_prom = self.__build_query_label_prefetch_related(qs=qs_coins_prom)
        qs_coins_prom = self.__sorting_coins(
            qs=qs_coins_prom,
            sort_option=sort_field,
            sort=sort_direction
        )

        # Сохраняем результат в кеш
        cache.set(cache_key, qs_coins_prom, cache_ttl)
        logfire.info("Кэш установлен для coins_promoted_tables", ttl=cache_ttl)

        return qs_coins_prom

    def get_published_coins(self) -> tuple[QuerySet, dict[str, Any]]:
        qs_coins = Coin.objects.filter(is_published=True)
        qs_coins = self.__build_query_select_related(qs=qs_coins)

        qs_coins = self.__filter_coins(
            qs=qs_coins,
            **self.client_params.filter_options.model_dump(),
            chain_slug=self.client_params.chain_slug
        )
        qs_coins = self.__sorting_coins(
            qs=qs_coins,
            sort_option=self.client_params.sort_field.value,
            sort=self.client_params.sort_direction.value
        )

        pagination_data, page_obj = self._create_pagination_data(
            qs=qs_coins,
            per_page=self.client_params.per_page,
            current_page_number=self.client_params.page_num
        )
        qs_coins_page = page_obj.object_list
        # Делаем prefetch после пагинации для оптимизации запроса:
        qs_coins = self.__build_query_label_prefetch_related(qs=qs_coins_page)

        return qs_coins, pagination_data

    def test_orm(self):
        reset_queries()

        qs_published, pagination_data = self.get_published_coins()
        qs__promoted = self.get_promoted_coins()
        top_tables = self.get_coins_tops_tables()


        data = {
            "pagination_data": pagination_data,
            "main_coins": list(qs_published),
            "promoted_coins": list(qs__promoted),
            "top_tables": top_tables
        }

        self.__debug_sql()

        return data
