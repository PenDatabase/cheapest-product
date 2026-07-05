from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from typing import Optional
from uuid import UUID
from .admin import setup_admin
from .database import Base, engine
from .dependencies import get_db
from . import models
from . import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

setup_admin(app, engine)


@app.get("/api/items", response_model=list[schemas.ItemListResponse])
def get_items(search: Optional[str] = None, db: Session = Depends(get_db)):
    query = select(models.Item).options(selectinload(models.Item.shop))

    if search:
        query = query.where(models.Item.name.ilike(f"%{search}%"))

    query = query.order_by(models.Item.price)
    items = db.scalars(query).all()

    return items


@app.get("/api/items/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: UUID, db: Session = Depends(get_db)):
    query = select(models.Item).where(models.Item.id == item_id)
    item = db.scalar(query)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item