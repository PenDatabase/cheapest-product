from .database import Base
from sqlalchemy import String, ForeignKey, Numeric, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from decimal import Decimal
from enum import Enum

class Feeling(str, Enum):
    HAPPY = "happy"
    NORMAL = "normal"
    SAD = "sad"
    ANGRY = "angry"


class Shop(Base):
    __tablename__ = "shops"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    display_name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(20))

    items: Mapped[list["Item"]] = relationship(back_populates="shop")


class Item(Base):
    __tablename__ = "items"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255))

    shop_id: Mapped[UUID] = mapped_column(ForeignKey("shops.id"))
    shop: Mapped["Shop"] = relationship(back_populates="items")

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    @property
    def shop_name(self) -> str:
        return self.shop.display_name


class Feedback(Base):
    __tablename__ = "feedback"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    feeling: Mapped[Feeling] = mapped_column(SQLEnum(Feeling))
    comment: Mapped[str] = mapped_column(Text)