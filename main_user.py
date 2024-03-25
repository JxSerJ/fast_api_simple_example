"""
Создать веб-страницу для отображения списка пользователей. Приложение
должно использовать шаблонизатор Jinja для динамического формирования HTML
страницы.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте HTML шаблон для отображения списка пользователей. Шаблон должен
содержать заголовок страницы, таблицу со списком пользователей и кнопку для
добавления нового пользователя.
Создайте маршрут для отображения списка пользователей (метод GET).
Реализуйте вывод списка пользователей через шаблонизатор Jinja.

"""
import hashlib

import uvicorn
from fastapi import FastAPI, HTTPException

from typing import Optional, List
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    email: Optional[str]
    password: str


def generate_password_hash(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def user_list_generator():
    result = []
    for i in range(4):
        id_ = i
        username = "user_" + str(i)
        email = str(username) + '@mail.mail'
        password = generate_password_hash('pass_' + str(i))
        data = {"id": id_, "username": username, "email": email, "password": password}
        user = User(**data)
        result.append(user)

    return result


user_list = user_list_generator()


@app.get("/")
async def root():
    return {"message": "root"}


@app.get("/users", response_model=List[User])
async def users():
    return user_list


@app.post("/new_user", response_model=User)
async def create_movie(user: User):
    user.password = generate_password_hash(user.password)
    user_list.append(user)
    return user


@app.put("/users/{username}", response_model=User)
async def update_movie(username: int, user: User):
    for index, user_ in enumerate(user_list):
        if user_.username == username:
            user_.password = generate_password_hash(user.password)
            user_list[index] = user_
            return user_
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{movie_id}")
async def delete_task(username: int):
    for index, user_ in enumerate(user_list):
        if user_.username == username:
            del user_list[index]
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")


if __name__ == '__main__':
    uvicorn.run("main_user:app", host='127.0.0.1', port=80, reload=True)
