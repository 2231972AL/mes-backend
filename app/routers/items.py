from fastapi import APIRouter

router = APIRouter(
    prefix="/items",
    tags=["items"]
)

@router.get("/")
def get_items():
    return [{"id": 1, "name": "Martello"}, {"id": 2, "name": "Chiave"}]
