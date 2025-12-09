from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserResponse
from app.utils.storage import users, user_id_counter

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserResponse)
def create_user(payload: UserCreate):
    global user_id_counter
    new_user = {
        "id": user_id_counter,
        "name": payload.name,
        "email": payload.email
    }
    users.append(new_user)
    user_id_counter += 1
    return new_user

@router.get("/", response_model=list[UserResponse])
def get_users():
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    for user in users:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


