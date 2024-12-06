import requests
from app.database import async_session_maker
from sqlalchemy import select, insert
from app.config import settings


class BaseDAO:
    model = None
    
    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            added_user = result.mappings().first()  
            return {"user added": added_user}
            
    
    @classmethod
    async def create_random_user(cls):
        response = requests.get(settings.RANDOM_USER_API_URL)
        if response.status_code == 200:
            user_data = response.json()['results'][0]
            result = await cls.add(
                city=user_data['location']['city'],
                username=user_data['login']['username'],
                password=user_data['login']['password']
            )
            return result
        else:
            raise ValueError("Failed to fetch random user")
        

    @classmethod
    async def find_one_or_none(cls,**filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
        
    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()
        

    @classmethod
    async def delete_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            user = result.scalar_one_or_none()

            if user:
                await session.delete(user)
                await session.commit()
                return {"message": f"User with id {model_id} has been deleted"}
            else:
                return {"error": f"User with id {model_id} not found"}