from django.urls import path

from app.views.app.api.add_coin.add_coin_data_view import add_coin_view, check_data_form
from app.views.app.api.coin_table_filters.coin_filter_view import coin_table_filter_view
from app.views.app.api.search_coin.search_coin_view import search_coin_name_view

# api-app-v1/
urlpatterns = [
    path(route='coin-table/filter-view/', view=coin_table_filter_view, name='coin_table_filter_view'),
    path(route='search-coin/name/', view=search_coin_name_view, name='search_coin_name_view'),

    path(route='add-coin/', view=add_coin_view, name='add_coin_view'),
    path(route='check-data-form/', view=check_data_form, name='check_data_form'),

]

