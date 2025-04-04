from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
async def log_in():
    pass

@router.post("/sign-up")
async def sign_up():
    pass
