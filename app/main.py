from .database import Base, engine
import app.models
from .dependencies import get_db
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Item
from typing import Optional
from uuid import UUID


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/api/items")
def get_items(search: Optional[str] = None, db: Session = Depends(get_db)):
    query = select(Item)

    if search:
        query = query.where(Item.name.ilike(f"%{search}%"))

    query = query.order_by(Item.price)
    items = db.scalars(query).all()

    return items


@app.get("/api/items/{item_id}")
def get_item(item_id: UUID, db: Session = Depends(get_db)):
    query = select(Item).where(Item.id == item_id)
    item = db.scalar(query)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item