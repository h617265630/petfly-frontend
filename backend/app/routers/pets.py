"""
宠物路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.curd import crud

router = APIRouter()

@router.post("/", response_model=schemas.PetResponse)
def create_pet(pet: schemas.PetCreate, db: Session = Depends(get_db)):
    """创建宠物"""
    return crud.PetCRUD.create(db, pet.model_dump())

@router.get("/", response_model=list[schemas.PetResponse])
def list_pets(owner_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取用户的宠物列表"""
    return crud.PetCRUD.get_by_owner(db, owner_id, skip, limit)

@router.get("/{pet_id}", response_model=schemas.PetResponse)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    """获取宠物详情"""
    pet = crud.PetCRUD.get_by_id(db, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="宠物不存在")
    return pet

@router.put("/{pet_id}", response_model=schemas.PetResponse)
def update_pet(pet_id: int, pet_update: schemas.PetUpdate, db: Session = Depends(get_db)):
    """更新宠物信息"""
    pet = crud.PetCRUD.get_by_id(db, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="宠物不存在")
    return crud.PetCRUD.update(db, pet, pet_update.model_dump(exclude_unset=True))

@router.delete("/{pet_id}")
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    """删除宠物"""
    pet = crud.PetCRUD.get_by_id(db, pet_id)
    if not pet:
        raise HTTPException(status_code=404, detail="宠物不存在")
    crud.PetCRUD.delete(db, pet_id)
    return {"message": "删除成功"}
