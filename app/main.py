from .database import Base, engine
from . import models
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from typing import Optional
from uuid import UUID
from .models import Item
from .dependencies import get_db
from . import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/api/items", response_model=list[schemas.ItemListResponse])
def get_items(search: Optional[str] = None, db: Session = Depends(get_db)):
    query = select(Item).options(selectinload(Item.shop))

    if search:
        query = query.where(Item.name.ilike(f"%{search}%"))

    query = query.order_by(Item.price)
    items = db.scalars(query).all()

    return items


@app.get("/api/items/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: UUID, db: Session = Depends(get_db)):
    query = select(Item).where(Item.id == item_id)
    item = db.scalar(query)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item