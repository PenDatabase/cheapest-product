from pydantic import BaseModel, Field, ConfigDict, AliasPath
from uuid import UUID
from decimal import Decimal

class ItemListResponse(BaseModel):
    id: UUID
    name: str
    price: Decimal
    shop_name: str
    shop_address: str
    model_config = ConfigDict(from_attributes=True)

class ShopResponse(BaseModel):
    id: UUID
    display_name: str
    address: str
    phone_number: str

class ItemResponse(BaseModel):
    id: UUID
    name: str
    price: Decimal
    shop: ShopResponse