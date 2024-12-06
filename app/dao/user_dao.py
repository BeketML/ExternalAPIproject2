from app.models import UserModel
from app.dao.base import BaseDAO


class UserDAO(BaseDAO):
    model = UserModel

