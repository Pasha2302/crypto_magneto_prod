from django.urls import path

from app.views.app.additional.contact_page.contact_view import contact_page_view
from app.views.app.additional.disclaimer_view import disclaimer_page_view
from app.views.app.additional.privacy_view import privacy_page_view
from app.views.app.additional.terms_and_conditions_view import terms_page_view
from app.views.app.coins.add_coin_page.add_coin_view import add_coin_page_view
from app.views.app.coins.coin_page.coin_view import coin_page_view
from app.views.app.index_page.index_view import index_page_view


urlpatterns = [
    path('', index_page_view, name='index_page_view'),
    path('token/<slug:chain_symbol>/<slug:coin_slug>', coin_page_view, name='coin_page_view'),

    path('submit-token/', add_coin_page_view, name='add_coin_page_view'),

    path('contact/', contact_page_view, name='contact_page_view'),
    path('privacy/', privacy_page_view, name='privacy_page_view'),
    path('terms-and-conditions/', terms_page_view, name='terms_page_view'),
    path('disclaimer/', disclaimer_page_view, name='disclaimer_page_view'),

    # path('test-page/', test_page_view, name='test_page_view'),
]
