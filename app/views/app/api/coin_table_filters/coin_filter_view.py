import logging

from django.http import HttpRequest, JsonResponse
from django.template.loader import render_to_string

from app.views.app.contexts.coin_context.table_coin_data.data_manager import CoinDataManager
from app.views.app.contexts.coin_context.table_coin_data.queries.queries_coin_table import TableCoinParamsService

logger = logging.getLogger("app.views")


class FilterTableContextManager:
    def __init__(self, request: HttpRequest):
        self.request = request
        self.__client_params = TableCoinParamsService.parse_from_request(self.request)
        self.__context = {}

    @staticmethod
    def __set_main_table_data(context, client_params):
        coin_data_manager = CoinDataManager(client_params)
        main_coins, pagination_data = coin_data_manager.get_published_coins()

        context['coins'] = main_coins
        context['pagination_data'] = pagination_data
        context['pagination_data']['per_page_datas'] = coin_data_manager.get_per_page_datas()
        context['filt_and_sort'] = coin_data_manager.get_filter_and_sorted_data_table()

    @staticmethod
    def __set_promoted_table_data(context, client_params):
        coin_data_manager = CoinDataManager(client_params)
        context['coins'] = coin_data_manager.get_promoted_coins()
        context['filt_and_sort'] = coin_data_manager.get_filter_and_sorted_data_table(only_columns=True)

    def get_context(self):
        if self.__client_params.promoted_only:
            self.__set_promoted_table_data(self.__context, self.__client_params)
        else:
            self.__set_main_table_data(self.__context, self.__client_params)

        return self.__context


# ===================== View =====================

def coin_table_filter_view(request: HttpRequest):
    if request.method == "GET":
        return JsonResponse(data={'error': 'Method Not Allowed' }, status=405)

    context = FilterTableContextManager(request).get_context()
    html_data = render_to_string(
        template_name='app/site/pages/index/components/main_table/main_table_wrapp.dj.html', context=context
    )
    data = {'html': html_data}

    return JsonResponse(data, status=200)


