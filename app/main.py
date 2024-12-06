from fastapi import APIRouter, FastAPI, HTTPException
import httpx
from app.config import settings
from app.routers.users import router as router_users
from app.routers.admins import router as router_admins

app = FastAPI()

test_api_router = APIRouter(
    tags=["Test API"]  
)

@app.get("/api-status")
async def check_api_status():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.RANDOM_USER_API_URL)
        
        response.raise_for_status()  
        return {"status": "API is connected and working properly"}
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail="External API error")
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="External API is not reachable")
    
app.include_router(router_admins)
app.include_router(router_users)