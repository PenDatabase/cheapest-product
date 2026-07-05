from sqladmin import Admin
from app.admin.views import ShopAdmin, ItemAdmin, FeedbackAdmin
from app.config import settings
from .auth import AdminAuth

def setup_admin(app, engine):
    authentication_backend = AdminAuth(settings.SECRET_KEY)
    admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)
    admin.add_view(ShopAdmin)
    admin.add_view(ItemAdmin)
    admin.add_view(FeedbackAdmin)