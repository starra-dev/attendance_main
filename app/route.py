from fastapi import APIRouter
import json


router = APIRouter()

@router.get("/data")
def load_data():
     with open (data.json, "r") as f:
        data = json.load()


@router.post("/data")
def save_data():
    with open (data.json, "w") as f:
        data = json.dump()