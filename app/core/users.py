import asyncio
from datetime import datetime, timedelta
import enum
import random
import uuid

from app.core.config import CONFIG

class UserLevel(enum.Enum):
    ADMIN = enum.auto()
    MODERATOR = enum.auto()
    USER = enum.auto()
    GUEST = enum.auto()

class Users():
    __tokens = {}
    async def is_valid_user(self, password : str) -> bool | str:
        # If the password is ok
        if password == CONFIG.ADMIN_PASSWORD and CONFIG.ADMIN_PASSWORD:
            return self.get_token()
        # Wait up to 2 seconds to throw off people trying to brute force
        delay_time = random.random() * 2
        await asyncio.sleep(delay_time)
        return False
        
    async def is_valid_token(self, token : str) -> bool:
        expiry_date = self.__tokens.get(token, None)
        if not expiry_date:
            return False
        if expiry_date < datetime.now():
            self.__tokens.pop(token)
            return False
        return True
    
    def get_token(self):
        expiry_date = datetime.now() + timedelta(hours = 12)
        token = str(uuid.uuid4())
        self.__tokens[token] = expiry_date
        return token

USERS = Users()