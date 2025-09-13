from fastapi import APIRouter

router = APIRouter()

@router.get("/home")
async def index():
    return {'message': "Page is running"}