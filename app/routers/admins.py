from fastapi import APIRouter, HTTPException, Response, status, Depends
from pydantic import BaseModel, EmailStr
from app.dao.admin_dao import AdminDAO
from app.models import AdminModel
from app.routers.auth import authenticate_user, get_current_admin, get_password_hash,create_access_token

router = APIRouter(
    prefix = "/auth",
    tags = ["Auth & Admins"]
)

class AdminAuthSchema(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register_user(user_data: AdminAuthSchema):
    existing_user = await AdminDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    
    hashed_password = get_password_hash(user_data.password)
    await AdminDAO.add(email=user_data.email, hashed_password=hashed_password)
    return {"message": "User successfully registered"}

@router.post("/login")
async def login_user(response: Response, user_data: AdminAuthSchema):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return {"access_token": access_token}

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return {"message": "Successfully logged out"}

@router.get("/me")
async def read_users_me(current_user: AdminModel = Depends(get_current_admin)):
    return current_user