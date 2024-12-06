from app.models import AdminModel
from app.dao.base import BaseDAO


class AdminDAO(BaseDAO):
    model = AdminModel

