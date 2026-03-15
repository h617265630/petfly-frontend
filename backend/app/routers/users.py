"""
用户路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.curd import crud

router = APIRouter()

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    existing = crud.UserCRUD.get_by_phone(db, user.phone)
    if existing:
        raise HTTPException(status_code=400, detail="手机号已注册")
    
    user_data = user.model_dump()
    user_data["role"] = user_data.get("role", "OWNER")
    return crud.UserCRUD.create(db, user_data)

@router.post("/login", response_model=schemas.UserResponse)
def login(phone: str, db: Session = Depends(get_db)):
    """登录（手机号验证码登录）"""
    user = crud.UserCRUD.get_by_phone(db, phone)
    if not user:
        # 自动注册
        user = crud.UserCRUD.create(db, {"phone": phone})
    return user

@router.get("/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """获取用户信息"""
    user = crud.UserCRUD.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@router.put("/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    """更新用户信息"""
    user = crud.UserCRUD.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return crud.UserCRUD.update(db, user, user_update.model_dump(exclude_unset=True))

@router.get("/", response_model=list[schemas.UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取用户列表"""
    return crud.UserCRUD.get_all(db, skip, limit)

# ============ 培飞员信息 ============
@router.get("/{user_id}/flyer-profile", response_model=schemas.FlyerProfileResponse)
def get_flyer_profile(user_id: int, db: Session = Depends(get_db)):
    """获取培飞员详细信息"""
    profile = db.query(crud.models.FlyerProfile).filter(
        crud.models.FlyerProfile.user_id == user_id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="培飞员信息不存在")
    return profile

@router.post("/{user_id}/flyer-profile", response_model=schemas.FlyerProfileResponse)
def create_flyer_profile(user_id: int, profile: schemas.FlyerProfileCreate, db: Session = Depends(get_db)):
    """创建培飞员信息"""
    existing = db.query(crud.models.FlyerProfile).filter(
        crud.models.FlyerProfile.user_id == user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="培飞员信息已存在")
    
    profile_data = profile.model_dump()
    profile_data["user_id"] = user_id
    new_profile = crud.models.FlyerProfile(**profile_data)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile
