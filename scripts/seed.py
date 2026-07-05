from faker import Faker
from app.database import Base, engine, SessionLocal
from sqlalchemy import insert
from sqlalchemy.orm import Session
from app.models import Shop, Item
import random
from decimal import Decimal
import asyncio

fake = Faker()

async def seed_shops(db: Session, count=10):
    shops = []
    for i in range(count):
        shop = Shop(
            display_name=fake.company(),
            address = fake.address(),
            phone_number=fake.phone_number()[:20]
        )
        db.add(shop)
        shops.append(shop)
        print(f"Shop{i} added")
    
    await db.flush()
    return shops


async def seed_items(db, shops: list[Shop], min_items, max_items):
    for shop in shops:
        item_count = random.randint(min_items, max_items)
        for i in range(item_count):
            item = Item(
                name = fake.word(),
                price = Decimal(random.randint(1000, 50000)),
                shop_id = shop.id,
            )
            db.add(item)
            print(f"Item{i} added successfully")


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        shops = await seed_shops(db, count=10)
        await seed_items(db, shops, 3, 5)
        await db.commit()
        print("Database Seeded")
    except Exception as e:
        await db.rollback()
        print(e)
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())