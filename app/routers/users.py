from fastapi import FastAPI, HTTPException, Depends,APIRouter
from pydantic import BaseModel
from app.database import async_session_maker, AsyncSession
import requests
from app.models import AdminModel, UserModel
from typing import Annotated, Optional
from app.config import settings
from sqlalchemy import select
from app.dao.user_dao import UserDAO
from app.routers.auth import get_current_admin

router = APIRouter(
    tags = ["Users"]
)

async def get_session():
    async with async_session_maker() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class UserCreateSchema(BaseModel):
    city: str
    username: str
    password: str

class UserGetSchema(BaseModel):
    id: int
    city: str
    username: str

class UserUpdateSchema(BaseModel):
    city: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


@router.post("/users/")
async def create_random_user(current_user: AdminModel = Depends(get_current_admin)):
    try:
        user = await UserDAO.create_random_user()
        return user
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/users")
async def read_users(current_user: AdminModel = Depends(get_current_admin)):
    user = await UserDAO.find_all()
    if user is None:
        raise HTTPException(status_code=404, detail="Users not found")
    return user

@router.get("/users/{user_id}")
async def read_user_by_id(user_id: int,current_user: AdminModel = Depends(get_current_admin)):
    user = await UserDAO.find_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
async def delete_user(user_id: int,current_user: AdminModel = Depends(get_current_admin)):
    user = await UserDAO.delete_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user