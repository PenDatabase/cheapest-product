from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from uuid import UUID
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from .admin import setup_admin
from .database import Base, engine
from .dependencies import get_db
from . import models
from . import schemas

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

setup_admin(app, engine)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/items", response_model=list[schemas.ItemListResponse])
async def get_items(search: Optional[str] = None, db: AsyncSession = Depends(get_db)):
    query = select(models.Item).options(selectinload(models.Item.shop))

    if search:
        query = query.where(models.Item.name.ilike(f"%{search}%"))

    query = query.order_by(models.Item.price)
    result = await db.scalars(query)
    items = result.all()

    return items


@app.get("/api/items/{item_id}", response_model=schemas.ItemResponse)
async def get_item(item_id: UUID, db: AsyncSession = Depends(get_db)):
    query = select(models.Item).options(selectinload(models.Item.shop)).where(models.Item.id == item_id)
    item = await db.scalar(query)

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item