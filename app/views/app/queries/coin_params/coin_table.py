from pydantic import BaseModel, Field, conint   #  pip install pydantic
from enum import Enum
from typing import Optional


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


class SortField(str, Enum):
    PRICE = "price"
    MARKET_CAP = "market_cap"
    VOLUME = "volume_usd"
    CHANGE = "price_change_24h"
    LAUNCH_DATE = "launch_date"


class CoinQueryParams(BaseModel):
    sort_field: SortField = Field(default=SortField.PRICE)
    sort_direction: SortDirection = Field(default=SortDirection.DESC)
    page: conint(ge=1) = Field(default=1)
    per_page: conint(ge=1, le=100) = Field(default=20)
    chain_symbol: Optional[str] = None
    promoted_only: Optional[bool] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
