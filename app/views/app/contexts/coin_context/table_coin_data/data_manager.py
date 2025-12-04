from pprint import pprint
from django.core.paginator import Paginator
from django.db.models import Prefetch, QuerySet, Case, When, Value, IntegerField
from django.db import connection, reset_queries

from app.db_models import Coin, Label


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
       - print_coin: выводит информацию о монетах и их метках в консоль.
       - _create_pagination_data: возвращает словарь с данными для пагинации.
       - __debug_sql: выводит все SQL-запросы, выполненные в текущей сессии Django ORM.

    Особенности реализации:
    - select_related + only ограничивает поля основной и связанных моделей, улучшая производительность JOIN.
    - Prefetch используется для связанных меток, чтобы минимизировать количество запросов к БД.
    - Пагинация реализована через django.core.paginator.Paginator с параметрами по умолчанию: 50 элементов на страницу.
    - Методы построены так, чтобы можно было отдельно получать промо-коины и
        обычные опубликованные монеты, не влияя друг на друга.
    """

    def __init__(self, client_params_table_filter):
        self.client_params_table_filter = client_params_table_filter

    @staticmethod
    def __debug_sql():
        print("\n SQL:\n")
        for q in connection.queries:
            print(q['sql'])
            print('==' * 50)

    @staticmethod
    def print_coin(coins_obj: list[Coin]):
        for coin_obj in coins_obj:
            labels_coin = None
            if hasattr(coin_obj, 'labels_coin'):
                labels_coin = [{"name": label.name, "slug": label.slug} for label in coin_obj.labels_coin if label]

            print(
                f"Name: {coin_obj.name}\n"
                f"Symbol: {coin_obj.symbol}\n"
                f"Contract Address: {coin_obj.contract_address}\n"
                f"Chain: {coin_obj.chain.name} [{coin_obj.chain.symbol}]\n"
                f"Price: {coin_obj.price}\n"
                f"Labels Coin: {labels_coin}\n"
            )
            print("==" * 60)

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
                # paginator_obj.get_elided_page_range(number=page_obj.number, on_each_side=2, on_ends=1)
                paginator_obj.get_elided_page_range(number=page_obj.number)
            ),
            "total_items": paginator_obj.count,
            "per_page": per_page,
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

                'name', 'symbol', 'contract_address', 'price', 'format_price', 'price_change_24h',
                'market_cap', 'volume_usd', 'volume_btc',


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
    def __sorting_coins(qs: QuerySet, sort_option: str, sort: str):
        order_prefix = '-' if sort == 'DESC' else ''
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

    def get_coins_tops_tables(self):
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

        return {
            'trending': list(self.__build_query_select_related(qs_trending)),
            'most_viewed': list(self.__build_query_select_related(qs_most_viewed)),
            'top_gainers': list(self.__build_query_select_related(qs_top_gainers)),
        }

    def get_promoted_coins(self):
        qs_coins_prom = Coin.objects.filter(promoted__isnull=False)
        qs_coins_prom = self.__build_query_select_related(qs=qs_coins_prom)
        qs_coins_prom = self.__build_query_label_prefetch_related(qs=qs_coins_prom)
        return qs_coins_prom

    def get_published_coins(self) -> QuerySet:
        qs_coins = Coin.objects.filter(is_published=True)
        qs_coins = self.__build_query_select_related(qs=qs_coins)
        qs_coins = self.__sorting_coins(qs=qs_coins, sort_option='price', sort='DESC')

        pagination_data, page_obj = self._create_pagination_data(qs_coins, self.per_page, self.current_page_number)
        qs_coins_page = page_obj.object_list
        # Делаем prefetch после пагинации для оптимизации запроса:
        qs_coins = self.__build_query_label_prefetch_related(qs=qs_coins_page)

        print("All Count Coins:\n")
        pprint(pagination_data)
        print("==" * 60)

        return qs_coins

    def test_orm(self):
        reset_queries()

        qs_published = self.get_published_coins()
        qs__promoted = self.get_promoted_coins()
        top_tables = self.get_coins_tops_tables()

        data = {
            "main_coins": list(qs_published),
            "promoted_coins": list(qs__promoted),
            "top_tables": top_tables
        }

        self.__debug_sql()

        return data
