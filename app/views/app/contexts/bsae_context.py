import logging
from django.http import HttpRequest

from app.db_models import BaseCoin, Coin
from app.db_models.site_models import ImageSite, ImageSocial
from app.views.app.contexts.coin_context.tools import format_float, format_int

logger = logging.getLogger(__name__)


class BaseContextManager:
    def __init__(self, request: HttpRequest, name_page: str | None = None):
        self.request = request
        self.cookies = request.COOKIES
        self.context = {}
        self.name_p = name_page

    @staticmethod
    def __get_data_menu(name_p: str):
        data_m = [
            {
                'name': 'Home', 'url': 'index_page_view',
                'status': 'active', 'class': '', 'slug': '',
            },
            {
                'name': 'Contacts', 'url': 'contact_page_view',
                'status': '', 'class': '', 'slug': '',
            },
            {
                'name': 'Privacy', 'url': 'privacy_page_view',
                'status': '', 'class': '', 'slug': '',
            },
            {
                'name': 'Terms', 'url': 'terms_page_view',
                'status': '', 'class': '', 'slug': '',
            },
            {
                'name': 'Disclaimer', 'url': 'disclaimer_page_view',
                'status': '', 'class': '', 'slug': '',
            },
        ]

        menu_btn = [
            {
                'name': 'Promote', 'label': 'Promote your coin',
                'cls': 'btn-header btn-promote',
                'url': 'terms_page_view',
            },
            {
                'name': 'Submit Token', 'label': 'Submit a new token',
                'cls': 'btn-header btn-submit',
                'url': 'add_coin_page_view',
            },
        ]

        return {"nav_m": data_m, "btn_m": menu_btn}

    @staticmethod
    def __get_social_img():
        qs_img = ImageSocial.objects.all()
        return {
            'socials': [
                {'name': img.name, 'slug': img.slug, 'url': img.image.url} for img in qs_img
                if img.image
            ]
        }

    def get_images_for_pages(self) -> dict[str, ImageSite]:
        names_pages = ['base', ]
        if self.name_p: names_pages.append(self.name_p)
        data_img = {
            obj.name: obj for obj in ImageSite.objects.filter(name_page__in=names_pages)
            if obj.image is not None
        }

        return data_img | self.__get_social_img()

    def __get_data_meta_tags(self, base_img_obj):
        base_img_url = base_img_obj.img_240.url if base_img_obj else ''
        return {
            # Заголовок страницы, используется в og:title и twitter:title
            "title": "AstroWhales | Whale Alert Signals",
            # Описание страницы, используется в og:description, twitter:description и meta name="description"
            "description": (
                "Our Whale Tracker is designed to help you monitor large transactions and understand "
                "their impact on the crypto market. Get live updates and follow your favorite token."
            ),
            # URL текущей страницы, используется в og:url
            "url": self.request.build_absolute_uri("/"),
            # URL изображения, используется в og:image и twitter:image
            "image_url": self.request.build_absolute_uri(base_img_url),
            # Альтернативный текст для изображения, используется в twitter:image:alt
            "image_alt": "AstroWhales site-image",
        }

    @staticmethod
    def __get_data_base_coin():
        datas = []

        for obj in BaseCoin.objects.all():
            datas.append({
                'symbol': obj.symbol,
                'price': format_float(obj.price),
            })

        return datas

    def get(self) -> dict:
        self.context["images_obj"] = self.get_images_for_pages()
        self.context["menu_items"] = self.__get_data_menu(self.name_p)
        self.context["meta"] = self.__get_data_meta_tags(self.context["images_obj"].get('main', ''))
        self.context['name_page'] = self.name_p
        self.context['base_coins'] = self.__get_data_base_coin()
        self.context['count_coins'] = format_int(Coin.objects.filter(is_published=True).count())

        return self.context


