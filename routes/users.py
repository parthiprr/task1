from fastapi import APIRouter

router = APIRouter()

users = []

# Create user
@router.post("/")
async def create_user(name: str):
    user = {
        "id": len(users) + 1,
        "name": name
    }
    users.append(user)
    return user

# Get all users
@router.get("/")
async def get_users():
    return users