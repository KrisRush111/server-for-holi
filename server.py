from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Временное хранилище пользователей (можно заменить на базу данных)
users: Dict[int, str] = {}

# Настройка CORS (чтобы `menu.html` мог делать запросы)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Можно указать конкретный домен, например "https://your-game.com"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель для запроса с Telegram-бота
class UserRequest(BaseModel):
    user_id: int
    user_name: str
    
@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Server is running"}

# Эндпоинт для сохранения имени пользователя
@app.post("/set_user/")
async def set_user(data: UserRequest):
    users[data.user_id] = data.user_name
    return {"message": f"Имя {data.user_name} сохранено!"}

# Эндпоинт для получения имени пользователя
@app.get("/get_user/{user_id}")
async def get_user(user_id: int):
    if user_id in users:
        return {"name": users[user_id]}
    else:
        return {"name": "Гость"}  # Если пользователя нет, вернуть "Гость"

# Тестовый роут (чтобы проверить, работает ли сервер)
@app.get("/")
async def root():
    return {"message": "Сервер работает!"}


