import os
import sys
import traceback
from typing import Union
from urllib.parse import urlparse

import httpx   # uv add httpx
from decimal import Decimal, InvalidOperation, ROUND_DOWN

MAX_PRICE = 10**12
MAX_MARKET_CAP = 10**15
MAX_LIQUIDITY = 10**15

if __name__ == '__main__':
    # Добавляем путь к корню проекта до импорта модулей
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
    django.setup()
    from django.conf import settings
    base_dir = settings.BASE_DIR
else:
    from django.conf import settings
    base_dir = settings.BASE_DIR

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.text import slugify
from app.db_models import Coin, Category, Label, ExplorerChain, Chain, PromotedCoin, BaseCoin
from django.db.models import Model
from django.db import models


def sanitize_decimal_value(value: Union[float, str, Decimal], model_instance: Model, field_name: str) -> Decimal:
    """
    Проверяет значение и возвращает либо его, либо максимально допустимое значение поля модели.

    :param value: Входное значение (может быть float, str, Decimal)
    :param model_instance: экземпляр модели (например, coin_obj)
    :param field_name: имя поля в модели (строка)
    :return: Decimal
    """
    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, TypeError):
        return Decimal('0.0')

    field = model_instance._meta.get_field(field_name)

    if not isinstance(field, models.DecimalField):
        raise TypeError(f"Поле {field_name} не является DecimalField")

    max_digits = field.max_digits
    decimal_places = field.decimal_places

    max_integer_digits = max_digits - decimal_places
    max_value = Decimal('9' * max_integer_digits + '.' + '9' * decimal_places)

    if abs(decimal_value) > max_value:
        return max_value
    return decimal_value


class CoinsImporter:
    headers = {'Accept': 'application/json',}
    def __init__(self, base_url: str, use_proxy: bool = False, log_file=None):
        self.log_file = log_file
        self.base_url = base_url
        self.proxy = "http://user130949:fduqey@195.2.248.140:8630" if use_proxy else None
        self.client = httpx.Client(headers=self.headers, timeout=40.0, verify=False, proxy=self.proxy)

    def write_log(self, str_log):
        if self.log_file:
            self.log_file.write(f'{str_log}\n')

    def fetch_page(self, url: str, params: dict | None = None) -> dict:
        try:
            resp = self.client.get(url, params=params)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            error_txt = f"[ERROR] Failed to fetch {url}: {e}"
            print(error_txt)
            self.write_log(error_txt)
            return {}

    @staticmethod
    def get_or_create_category(cat_data: dict) -> Category | None:
        if not cat_data or "name" not in cat_data: return None

        name = cat_data["name"]
        slug = slugify(name)
        category, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})
        return category

    @staticmethod
    def get_or_create_label(data: dict) -> Label | None:
        if not data or "name" not in data: return None

        name = data["name"]
        slug = slugify(name)
        label, _ = Label.objects.get_or_create(slug=slug, defaults={"name": name})
        return label

    def save_image(self, url: str, instance):
        if not url: return
        try:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(self.client.get(url).content)
            img_temp.flush()
            filename = os.path.basename(urlparse(url).path)
            instance.image.save(filename, File(img_temp), save=False)
        except Exception as e:
            error_txt = f"[ERROR] Failed to download/save image {url}: {e}"
            print(error_txt)
            self.write_log(error_txt)

    def get_or_create_contract_nad_chain(self, data: dict, obj_coin: Coin):
        if not data: return None

        explorer_obj = None
        chain_obj = None
        obj_coin.contract_address = data["contract_address"]
        chain_data = data.get("chain")

        if chain_data:
            chain_name = chain_data.get("name")
            chain_slug = chain_data.get("slug")
            chain_symbol = chain_data.get("symbol")
            chain_img = chain_data.get("path_chain_img")

            explorer_data = chain_data.get("explorer", {})
            if explorer_data:
                explorer_name = explorer_data.get("name")
                explorer_url = explorer_data.get("url")
                slug = slugify(explorer_name)
                explorer_obj , _ = ExplorerChain.objects.get_or_create(
                    slug=slug, defaults={"name": explorer_name, "url": explorer_url}
                )

            chain_obj, created = Chain.objects.get_or_create(
                slug=chain_slug, defaults={
                    "name": chain_name,
                    "symbol": chain_symbol,
                    "explorer": explorer_obj
                }
            )
            # если новая цепочка — загружаем изображение
            if created and chain_img:
                self.save_image(chain_img, chain_obj)
                chain_obj.save()

        obj_coin.chain = chain_obj

        return None

    @staticmethod
    def update_or_create_promoted(data_promoted: dict, obj_coin: Coin):
        if not isinstance(data_promoted, dict): return None

        PromotedCoin.objects.update_or_create(
            coin=obj_coin,
            defaults={
                "start_date": data_promoted.get("start_date"),
                "end_date": data_promoted.get("end_date"),
                "is_permanent": data_promoted.get("is_permanent"),
            }
        )
        return None

    @staticmethod
    def update_or_create_base_coins(base_coins_data: dict):
        BaseCoin.objects.update_or_create(
            slug=base_coins_data.get("slug"),
            defaults={
                "name": base_coins_data.get("name"),
                "symbol": base_coins_data.get("symbol"),
                "pair_url": base_coins_data.get("pair_url"),
                "price": base_coins_data.get("price"),
                "format_price": base_coins_data.get("format_price"),
            }
        )

    def process_coin(self, data: dict):
        if not data.get("name") or not data.get("symbol"):
            return

        slug = slugify(f"{data['name']}-{data['symbol']}", allow_unicode=True)

        try:
            coin, created = Coin.objects.get_or_create(slug=slug, defaults={
                "name": data["name"],
                "symbol": data["symbol"],
                "source_page": data.get("source_page"),
            })

            decimal_fields = [
                ("price", MAX_PRICE, 18),
                ("market_cap", MAX_MARKET_CAP, 2),
                ("liquidity_usd", MAX_LIQUIDITY, 2),
                ("volume_usd", MAX_LIQUIDITY, 2),
                ("volume_btc", None, 8),
            ]

            # --- Только Decimal-поля ---
            for field, max_value, decimal_places in decimal_fields:
                if field in data:
                    raw_value = data[field]
                    if raw_value is None:
                        setattr(coin, field, None)
                        continue
                    try:
                        value = Decimal(raw_value)
                        if max_value is not None and value > max_value:
                            value = Decimal(max_value)
                        value = value.quantize(Decimal("1." + "0" * decimal_places), rounding=ROUND_DOWN)
                        setattr(coin, field, value)
                    except (ValueError, InvalidOperation) as e:
                        error_txt = (f"[WARN coin | Name: {coin.name} | Symbol: {coin.symbol}]\n"
                                     f"Invalid Decimal for {field}: {raw_value} ({e})")
                        print(error_txt)
                        self.write_log(error_txt)
                        setattr(coin, field, None)

            # --- Остальные поля без специальной проверки ---
            for field in [
                "name", "symbol", "source_page", "market_cap_rank", "format_price",
                "market_cap_presale", "is_published", "launch_date", "last_price_update",
                "published_at", "popularity_rank", "popularity_updated_at",
                "security_updated_at", "gugu_rank",
                "price_change_24h", "price_change_1h", "buys_h1", "sells_h1",
                "buys_h24", "sells_h24", "views", "votes", "votes24h",
                "popularity_score", "security_score", "gugu_score"
            ]:
                if field in data:
                    setattr(coin, field, data[field])

            description = data.get("description", {})
            coin.full_desc = description.get('full_desc', '') if description else ''

            # Категории
            if "categories" in data:
                coin.categories.clear()
                for cat_data in data["categories"]:
                    category = self.get_or_create_category(cat_data)
                    if category:
                        coin.categories.add(category)

            # Метки
            if "labels" in data:
                coin.labels.clear()
                for label_data in data["labels"]:
                    label = self.get_or_create_label(label_data)
                    if label:
                        coin.labels.add(label)

            # Скачивание изображения
            if "img" in data and created:
                self.save_image(data["img"], coin)

            if "contract_address" in data:
                datas_address = data["contract_address"]
                if isinstance(datas_address, list):
                    for data_address in datas_address:
                        if  data_address.get("basic"):
                            self.get_or_create_contract_nad_chain(data_address, obj_coin=coin)

            if "promoted" in data:
                data_promoted = data.get("promoted")
                if data_promoted:
                    self.update_or_create_promoted(data_promoted, obj_coin=coin)

            coin.save()
            print(f"{'Created' if created else 'Updated'} coin: {coin.name}")

        except Exception as e:
            error_txt = (
                f"[ERROR] Failed to save coin {data.get('name')} ({slug}): {e}\n"
                f"{traceback.format_exc()}"
            )
            print(error_txt)
            self.write_log(error_txt)

    def run(self):
        next_url = self.base_url
        page_counter = 1
        base_coins_datas = []

        while next_url:
            # if page_counter == 2: break
            print(f"[INFO] Fetching page {page_counter}: {next_url}")
            data = self.fetch_page(next_url)

            match data:
                case {"results": list() as coins_data}:
                    for coin_data in coins_data:
                        self.process_coin(coin_data)
                case _:
                    error_txt = f"[ERROR] Unexpected data: {data}"
                    print(error_txt)
                    self.write_log(error_txt)

            next_url = data.get("next")
            page_counter += 1

            if not base_coins_datas:
                base_coins_datas = data.get("base_coins")

        if base_coins_datas:
            for base_coins in base_coins_datas:
                self.update_or_create_base_coins(base_coins_data=base_coins)


if __name__ == "__main__":
    with open("error.log", "a") as f:
        importer = CoinsImporter(
            base_url="https://cryptogugu.com/api/v1/drf/get-coins/?page_size=100",
            # base_url="http://127.0.0.1:8000/api/v1/drf/get-coins/?page_size=100",
            use_proxy=True,
            log_file=f
        )
        importer.run()

