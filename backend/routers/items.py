from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, schemas, database

router = APIRouter()

@router.get("/")
def read_items(db: Session = Depends(database.get_db)):
    return crud.get_items(db)

@router.post("/")
def create_item(item: schemas.ItemCreate, db: Session = Depends(database.get_db)):
    return crud.create_item(db, item)
