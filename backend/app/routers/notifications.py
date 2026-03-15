"""
通知路由
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.curd import crud

router = APIRouter()

@router.get("/", response_model=list[schemas.NotificationResponse])
def get_notifications(user_id: int, skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    """获取用户通知列表"""
    return crud.NotificationCRUD.get_by_user(db, user_id, skip, limit)

@router.get("/unread-count")
def get_unread_count(user_id: int, db: Session = Depends(get_db)):
    """获取未读数量"""
    return {"count": crud.NotificationCRUD.get_unread_count(db, user_id)}

@router.post("/{notification_id}/read")
def mark_as_read(notification_id: int, db: Session = Depends(get_db)):
    """标记为已读"""
    notif = crud.NotificationCRUD.mark_as_read(db, notification_id)
    if not notif:
        return {"message": "通知不存在"}
    return {"message": "已标记为已读"}

@router.post("/read-all")
def mark_all_as_read(user_id: int, db: Session = Depends(get_db)):
    """全部标记为已读"""
    crud.NotificationCRUD.mark_all_as_read(db, user_id)
    return {"message": "全部已读"}
