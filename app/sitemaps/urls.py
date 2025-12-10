from django.contrib.sitemaps.views import sitemap
from django.urls import path

from app.sitemaps.sitemaps import (
    CoinsSitemap, StaticViewSitemap, SitemapIndexView,
)

sitemaps = {
    'static': StaticViewSitemap(),
    'coin': CoinsSitemap(),
}


urlpatterns = [
    path('sitemap.xml', SitemapIndexView.as_view(), name='sitemap-index'),  # Главный сайтмап
    path(
        'sitemap-coins.xml',
        sitemap,
        {
            'sitemaps': {'coins': CoinsSitemap()},
            #'template_name': 'django.contrib.sitemaps/sitemap.xml',
        }, name='sitemap-coins'
    ),
    path(
        'sitemap-pages.xml',
        sitemap,
        {
            'sitemaps': {'static': StaticViewSitemap()},
            #'template_name': 'django.contrib.sitemaps/sitemap.xml',
        }, name='sitemap-pages'
    ),  # Страницы

]
