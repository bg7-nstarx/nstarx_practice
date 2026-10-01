from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt

app = FastAPI()

SECRET_KEY = "my-secret-key"
ALGORITHM = "HS256"

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

# Simple in-memory database
users = {}


class User(BaseModel):
    username: str
    password: str


@app.post("/register")
def register(user: User):

    if user.username in users:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    hashed_password = pwd_context.hash(user.password)

    users[user.username] = hashed_password

    return {
        "message": "Registration successful"
    }


@app.post("/login")
def login(user: User):

    if user.username not in users:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    stored_password = users[user.username]

    if not pwd_context.verify(
        user.password,
        stored_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = jwt.encode(
        {"username": user.username},
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return {
        "access_token": token
    }