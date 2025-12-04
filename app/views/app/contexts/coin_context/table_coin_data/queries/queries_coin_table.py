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


class TableCoinParamsService:

    @staticmethod
    def parse_from_request(request) -> TableCoinQueryParams:
        raw_data = parse_request_data(request)
        try:
            return TableCoinQueryParams(**raw_data)
        except ValidationError as e:
            raise ValueError(f"Invalid query params: {e}")





