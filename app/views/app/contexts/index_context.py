from django.http import HttpRequest
from app.views.app.contexts.bsae_context import BaseContextManager
from app.views.app.contexts.coin_context.table_coin_data.data_manager import CoinDataManager

from app.views.app.contexts.coin_context.table_coin_data.queries.queries_coin_table import TableCoinParamsService


class IndexContextManager:
    def __init__(self, request: HttpRequest):
        self.request = request
        self.__context = BaseContextManager(self.request, name_page='index').get()
        self.route_name = request.resolver_match.url_name
        self.__client_params_table_filter = TableCoinParamsService.parse_from_request(self.request, self.route_name)

    @staticmethod
    def __set_data_coins(context, client_params):
        print(f"\nClient params:\n{client_params}")
        coin_data_manager = CoinDataManager(client_params)

        main_coins, pagination_data = coin_data_manager.get_published_coins()

        context['pagination_data'] = pagination_data
        context['pagination_data']['per_page_datas'] = coin_data_manager.get_per_page_datas()
        context['main_coins'] = main_coins
        context['promoted_coins'] = coin_data_manager.get_promoted_coins()
        context['top_tables'] = coin_data_manager.get_coins_tops_tables()

        context['filt_and_sort'] = coin_data_manager.get_filter_and_sorted_data_table()

    def get(self):
        self.__set_data_coins(self.__context, self.__client_params_table_filter)
        self.__context['filter_page'] = self.route_name
        self.__context['is_filter_page'] = self.route_name in ("new", "presale", "doxxed", "audited", "List_tokens")
        return self.__context

