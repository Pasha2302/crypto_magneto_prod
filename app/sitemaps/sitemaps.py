from django.http import HttpResponse, HttpRequest
from django.utils.timezone import now

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from datetime import date

from django.views import View

from app.db_models import Coin


class SitemapIndexView(View):
    def get(self, request: HttpRequest):
        # Генерируем XML сайтмапа
        domain = request.build_absolute_uri('/')[:-1]  # Получаем текущий домен без слэша в конце
        today = now().date()

        xml = f'''<?xml version="1.0" encoding="UTF-8"?>
        <sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

            <sitemap>
                <loc>{domain}/sitemap-pages.xml</loc>
                <lastmod>{today}</lastmod>
            </sitemap>

            <sitemap>
                <loc>{domain}/sitemap-coins.xml</loc>
                <lastmod>{today}</lastmod>
            </sitemap>

        </sitemapindex>'''

        return HttpResponse(xml, content_type="application/xml")


class CoinsSitemap(Sitemap):

    def items(self):
        # Получаем все монеты из базы
        return Coin.objects.filter(is_published=True)

    def location(self, item: Coin):
        url = item.get_site_url(is_relative_path=True)  # Получаем базовый чейн
        return url

    def lastmod(self, item: Coin):
        return item.updated_at if hasattr(item, "updated_at") else date.today()


class StaticViewSitemap(Sitemap):

    def items(self):
        # Список имен маршрутов, которые нужно включить в сайтмап
        return [
            "add_coin_page_view",

            "new",
            "presale",
            "doxxed",
            "audited",

            "contact_page_view",
            "privacy_page_view",
            "terms_page_view",
            "disclaimer_page_view",
        ]

    def location(self, item):
        # Генерация URL на основе имени маршрута
        return reverse(item)

    def lastmod(self, item):
        # Возвращаем текущую дату как объект datetime.date
        return date.today()


# ================================================================================================================ #
