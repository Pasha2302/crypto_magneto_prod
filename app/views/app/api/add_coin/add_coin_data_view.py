from django.http import HttpRequest, JsonResponse
from django.utils.text import slugify

from app.db_models import Coin, Chain, CoinSocial, ImageSocial
from app.views.app.api.tools import parse_request_data

from datetime import date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, ConfigDict
from django.db import transaction
from pydantic import ValidationError
from datetime import datetime


class SocialData(BaseModel):
    """Модель для данных социальных сетей"""
    slug: str
    url: str


class AddCoinData(BaseModel):
    """Модель для валидации данных добавления монеты"""
    model_config = ConfigDict(
        arbitrary_types_allowed=True,  # Для поддержки UploadedFile
        from_attributes=True
    )

    name: str
    symbol: str
    full_desc: Optional[str] = None
    launch_date: Optional[date] = None
    chain: str
    contract_address: str

    # Для файлов и дополнительных данных
    socials_data: List[SocialData] = Field(default_factory=list)
    image_file: Optional[Any] = None  # UploadedFile

    @classmethod
    @field_validator("name", mode="before")
    def validate_name(cls, v: str) -> str:
        if not v or len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()

    @classmethod
    @field_validator("symbol", mode="before")
    def validate_symbol(cls, v: str) -> str:
        if not v or len(v.strip()) < 2:
            raise ValueError('Symbol must be at least 2 characters long')
        return v.upper().strip()

    @classmethod
    @field_validator('contract_address', mode="before")  # <mode="before"> -- это  ??
    def validate_contract_address(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError('Contract address is required')
        if not v.startswith('0x'):
            raise ValueError('Contract address must start with 0x')
        if len(v) < 10:
            raise ValueError('Invalid contract address')
        return v


class AddCoinResponse(BaseModel):
    """Модель для ответа после добавления монеты"""
    success: bool
    coin_id: Optional[int] = None
    message: Optional[str] = None
    errors: List[Dict[str, Any]] = Field(default_factory=list)


# ============================================================================================================ #

class AddCoinFromForm:
    def __init__(self, data_form, image_file):
        self.data_form = data_form
        self.image_file = image_file
        self.errors = []

    @staticmethod
    def __get_socials_data(data_form) -> List[SocialData]:
        """Извлекает данные социальных сетей из формы"""
        socials_data = []
        for key, value in data_form.items():
            if key.startswith('social_') and value:
                soc_slug = key.replace('social_', '')
                socials_data.append(SocialData(
                    slug=soc_slug,
                    url=value
                ))
        return socials_data

    def __validate_data(self) -> Optional[AddCoinData]:
        """Валидирует данные с помощью Pydantic"""
        try:
            # Преобразуем launch_date из строки в date
            launch_date_str = self.data_form.get('launch_date')
            launch_date = None
            if launch_date_str:
                try:
                    launch_date = datetime.strptime(launch_date_str, '%Y-%m-%d').date()
                except ValueError:
                    self.errors.append({
                        'field': 'launch_date',
                        'error': 'Invalid date format. Use YYYY-MM-DD'
                    })
                    return None

            # Получаем данные социальных сетей
            socials_data = self.__get_socials_data(self.data_form)

            # Создаем Pydantic модель
            coin_data = AddCoinData.model_validate({
                'name': self.data_form.get('name', '').strip(),
                'symbol': self.data_form.get('symbol', '').strip(),
                'full_desc': self.data_form.get('full_desc', '').strip(),
                'launch_date': launch_date,
                'chain': self.data_form.get('chain', '').strip(),
                'contract_address': self.data_form.get('contract_address', '').strip(),
                'socials_data': socials_data,
                'image_file': self.image_file
            })

            return coin_data

        except ValidationError as e:
            # Обрабатываем ошибки валидации Pydantic
            for error in e.errors():
                field = error['loc'][0] if error['loc'] else 'unknown'
                self.errors.append({
                    'field': field,
                    'error': error['msg']
                })
            return None

    def __check_duplicates(self, coin_data: AddCoinData) -> bool:
        """Проверяет на дубликаты в базе данных"""
        # Проверка по slug (имя + символ)
        slug = slugify(f"{coin_data.name}-{coin_data.symbol}", allow_unicode=True)
        if Coin.objects.filter(slug=slug).exists():
            self.errors.append({
                'field': 'name',
                'error': 'Coin with this name and symbol already exists!'
            })
            return False

        # Проверка по контрактному адресу
        if coin_data.contract_address:
            if Coin.objects.filter(contract_address=coin_data.contract_address).exists():
                self.errors.append({
                    'field': 'contract_address',
                    'error': 'This contract address already exists!'
                })
                return False

        return True

    @staticmethod
    def __save_social_links(coin: Coin, socials_data: List[SocialData]):
        """Сохраняет ссылки на социальные сети"""
        for social in socials_data:
            CoinSocial.objects.create(
                coin=coin,
                name=social.slug,
                url=social.url,
                image=ImageSocial.objects.get(slug=social.slug),
            )
            pass

    def __save_coin(self, coin_data: AddCoinData) -> Optional[Coin]:
        """Сохраняет монету в базу данных"""
        try:
            with transaction.atomic():
                # Получаем или создаем slug
                slug = slugify(f"{coin_data.name}-{coin_data.symbol}", allow_unicode=True)

                # Получаем объект Chain
                try:
                    chain = Chain.objects.get(slug__iexact=coin_data.chain)
                except Chain.DoesNotExist:
                    self.errors.append({
                        'field': 'chain',
                        'error': f'Chain "{coin_data.chain}" does not exist'
                    })
                    return None

                # Создаем монету
                coin = Coin.objects.create(
                    slug=slug,
                    name=coin_data.name,
                    symbol=coin_data.symbol,
                    contract_address=coin_data.contract_address,
                    chain=chain,
                    full_desc=coin_data.full_desc,
                    launch_date=coin_data.launch_date
                )

                # Сохраняем изображение если есть
                if coin_data.image_file:
                    coin.image.save(
                        coin_data.image_file.name,
                        coin_data.image_file,
                        save=True
                    )

                # Сохраняем социальные сети
                if coin_data.socials_data:
                    self.__save_social_links(coin, coin_data.socials_data)

                return coin

        except Exception as e:
            self.errors.append({
                'field': 'database',
                'error': f'Database error: {str(e)}'
            })
            return None

    def add(self) -> Dict[str, Any]:
        """Основной метод добавления монеты"""
        # Валидируем данные
        coin_data = self.__validate_data()
        if not coin_data:
            return {
                'success': False,
                'message': 'Validation failed',
                'errors': self.errors
            }

        # Проверяем на дубликаты
        if not self.__check_duplicates(coin_data):
            return {
                'success': False,
                'message': 'Duplicate found',
                'errors': self.errors
            }

        # Сохраняем в базу данных
        coin = self.__save_coin(coin_data)
        if not coin:
            return {
                'success': False,
                'message': 'Failed to save coin',
                'errors': self.errors
            }

        return {
            'success': True,
            'coin_id': coin.pk,
            'message': 'Coin added successfully',
            'errors': []
        }


# ============================================================================================================ #

def add_coin_view(request: HttpRequest):
    """View для добавления монеты"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method must be POST.'}, status=400)

    try:
        # Получаем данные из формы
        data_form = request.POST.dict()
        image_file = request.FILES.get("image")

        # Создаем экземпляр класса и добавляем монету
        add_coin = AddCoinFromForm(data_form, image_file)
        result = add_coin.add()

        # Возвращаем ответ
        if result['success']:
            return JsonResponse(result, status=200)
        else:
            return JsonResponse(result, status=400)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Internal server error',
            'errors': [{'field': 'system', 'error': str(e)}]
        }, status=500)


def check_data_form(request: HttpRequest):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method must be POST.'}, status=400)

    data_form = parse_request_data(request=request)
    print("\nData Form:\n", data_form)

    errors = []

    if data_form.get('name') and data_form.get('symbol'):
        name = data_form.get('name')
        symbol = data_form.get('symbol')
        slug = slugify(f"{name}-{symbol}", allow_unicode=True)
        if Coin.objects.filter(slug=slug).first():
            errors.append({
                'selectors_msg_error': '#error_name',
                'selectors_elms_error': ['#token-name', '#token-ticker'],
                'error_msg': 'This coin already exists!'
            })

    if data_form.get('contract_address') and data_form.get('chain'):
        contract_address = data_form.get('contract_address')
        if Coin.objects.filter(contract_address=contract_address).first():
            errors.append({
                'selectors_msg_error': '#error_contract',
                'selectors_elms_error': ['#contract-address'],
                'error_msg': 'This contract address already exists!'
            })

    # Возвращаем словарь с ошибками
    return JsonResponse(data={
        'success': len(errors) == 0,
        'errors': errors
    }, status=200)
