from fastapi import APIRouter, HTTPException, status
from app.schemas.user_schema import UserCreate, UserResponse
from app.utils.storage import users, user_id_counter

router = APIRouter(prefix="/users", tags=["Users"])

def _find_user_index(user_id: int):
    for index, user in enumerate(users):
        if user["id"] == user_id:
            return index
    return -1

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    global user_id_counter

    for user in users:
        if user["email"] == payload.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )
    
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
    index = _find_user_index(user_id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return users[index]

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserCreate):
    index = _find_user_index(user_id)
    if index == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details="User not found")

    stored_user = users[index]
    update_data = payload.model_dump(exclude_unset=True)

    if "email" in update_data:
        new_email = update_data["email"]
        for u in users:
            if u["id"] != user_id and u["email"] ==new_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    details="Email already exists",
                )
    users[index] = {**stored_user, **update_data}
    return users[index]

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    index = _find_user_index(user_id)
    if index == -1:
        raise HTTPExceptions(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found",
        )
    users.pop(index)
    return