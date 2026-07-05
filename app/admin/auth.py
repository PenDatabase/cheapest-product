from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request):
        return True
    
    async def logout(self, request: Request):
        return True
    
    async def authenticate(self, request: Request):
        return True