from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, conint, ValidationError, field_validator  # pip install pydantic

from app.views.app.api.tools import parse_request_data


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SortField(str, Enum):
    MARKET_CAP = "market_cap"
    VOLUME = "volume_usd"
    PRICE = "price"
    CHANGE = "price_change_24h"
    LAUNCH_DATE = "launch_date"


class FilteringOptions(BaseModel):
    new: bool = False
    presale: bool = False
    doxxed: bool = False
    audited: bool = False


class TableCoinQueryParams(BaseModel):
    sort_field: SortField = Field(default=SortField.PRICE)
    sort_direction: SortDirection = Field(default=SortDirection.DESC)
    filter_options: FilteringOptions = Field(default_factory=FilteringOptions)
    page_num: conint(ge=1) = Field(default=1)
    per_page: conint(ge=10, le=100) = Field(default=10)

    chain_slug: Optional[str] = None
    # Optional[bool] = None  --  Это полезно, если нужно различать три состояния (True, False, None):
    promoted_only: Optional[bool] = None  # Optional - позволяет задавать поле как -- None

    @classmethod
    @field_validator("*", mode="before")  # для всех полей
    def empty_to_none(cls, value):
        if value in ("", "null", "None"):
            return None
        return value

# ========================================================================================== #


def apply_filter_from_route_name(raw_data: dict, route_name: str) -> dict:
    """
    Если route_name совпадает с именем фильтра — включаем его.
    Например route_name="presale" -> filter_options.presale=True
    """
    # список доступных фильтров ровно как в FilteringOptions
    available_filters = {"new", "presale", "doxxed", "audited"}

    if route_name in available_filters:
        filter_opts = raw_data.setdefault("filter_options", {})
        filter_opts[route_name] = True

    return raw_data


class TableCoinParamsService:

    @staticmethod
    def parse_from_request(request, route_name='') -> TableCoinQueryParams:
        raw_data = parse_request_data(request)

        # применяем фильтр, если имя маршрута совпадает с фильтром
        raw_data = apply_filter_from_route_name(raw_data, route_name)

        try:
            return TableCoinQueryParams(**raw_data)
        except ValidationError as e:
            raise ValueError(f"Invalid query params: {e}")





