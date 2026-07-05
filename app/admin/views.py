from app.models import Shop, Item, Feedback
from sqladmin import ModelView

class ShopAdmin(ModelView, model=Shop):
    coulmn_list = [Shop.id, Shop.display_name, Shop.address, Shop.phone_number]

class ItemAdmin(ModelView, model=Item):
    column_list = [Item.id, Item.name, Item.price, Item.price, Item.shop_id]

class FeedbackAdmin(ModelView, model=Feedback):
    column_list = [Feedback.id, Feedback.feeling, Feedback.comment]