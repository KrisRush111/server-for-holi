from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def create_app():
    app = FastAPI()

    # Временное хранилище пользователей (можно заменить на базу данных)
    users: Dict[int, str] = {}

    # Настройка CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    class UserRequest(BaseModel):
        user_id: int
        user_name: str

    @app.post("/set_user/")
    async def set_user(data: UserRequest):
        users[data.user_id] = data.user_name
        logger.info(f"Пользователь {data.user_name} (ID: {data.user_id}) добавлен.")
        return {"message": f"Имя {data.user_name} сохранено!"}

    @app.get("/get_user/{user_id}")
    async def get_user(user_id: int):
        if user_id in users:
            return {"name": users[user_id]}
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    @app.get("/")
    async def root():
        return {"message": "Сервер работает"}

    @app.head("/")
    async def head_root():
        return Response(status_code=200)

    @app.get("/health")
    async def health_check():
        """Проверка состояния сервера"""
        return {"status": "ok"}

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
