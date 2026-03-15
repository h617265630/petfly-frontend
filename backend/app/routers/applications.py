"""
申请路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.curd import crud
from app.models import models

router = APIRouter()

@router.post("/", response_model=schemas.ApplicationResponse)
def create_application(application: schemas.ApplicationCreate, db: Session = Depends(get_db)):
    """创建申请"""
    # 检查任务是否存在
    task = crud.TaskCRUD.get_by_id(db, application.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if task.status != "OPEN":
        raise HTTPException(status_code=400, detail="只有开放的任务可以申请")
    
    # 检查是否已经申请过
    existing = crud.TaskApplicationCRUD.get_by_task_and_flyer(
        db, application.task_id, application.flyer_id
    )
    if existing:
        raise HTTPException(status_code=400, detail="您已经申请过这个任务")
    
    app_data = application.model_dump()
    new_app = crud.TaskApplicationCRUD.create(db, app_data)
    
    # 通知任务主人
    crud.NotificationCRUD.create(db, {
        "user_id": task.owner_id,
        "type": "APPLICATION_NEW",
        "title": "有新申请",
        "content": f"培飞员申请了您的任务",
        "related_id": new_app.id,
        "related_type": "application"
    })
    
    return new_app

@router.get("/task/{task_id}", response_model=list[schemas.ApplicationResponse])
def get_task_applications(task_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取任务的申请列表"""
    return crud.TaskApplicationCRUD.get_by_task(db, task_id, skip, limit)

@router.get("/my", response_model=list[schemas.ApplicationResponse])
def get_my_applications(flyer_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取我的申请列表"""
    return crud.TaskApplicationCRUD.get_by_flyer(db, flyer_id, skip, limit)

@router.get("/{application_id}", response_model=schemas.ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    """获取申请详情"""
    app = crud.TaskApplicationCRUD.get_by_id(db, application_id)
    if not app:
        raise HTTPException(status_code=404, detail="申请不存在")
    return app

@router.put("/{application_id}/accept", response_model=schemas.ApplicationResponse)
def accept_application(application_id: int, db: Session = Depends(get_db)):
    """接受申请（主人操作）"""
    app = crud.TaskApplicationCRUD.get_by_id(db, application_id)
    if not app:
        raise HTTPException(status_code=404, detail="申请不存在")
    
    app.status = "SHORTLISTED"
    db.commit()
    db.refresh(app)
    
    # 通知培飞员
    crud.NotificationCRUD.create(db, {
        "user_id": app.flyer_id,
        "type": "APPLICATION_ACCEPTED",
        "title": "申请已通过",
        "content": f"您的申请已被主人通过",
        "related_id": app.id,
        "related_type": "application"
    })
    
    return app

@router.put("/{application_id}/reject", response_model=schemas.ApplicationResponse)
def reject_application(application_id: int, reason: str = None, db: Session = Depends(get_db)):
    """拒绝申请（主人操作）"""
    app = crud.TaskApplicationCRUD.get_by_id(db, application_id)
    if not app:
        raise HTTPException(status_code=404, detail="申请不存在")
    
    app.status = "REJECTED"
    app.reject_reason = reason
    db.commit()
    db.refresh(app)
    
    # 通知培飞员
    crud.NotificationCRUD.create(db, {
        "user_id": app.flyer_id,
        "type": "APPLICATION_REJECTED",
        "title": "申请被拒绝",
        "content": f"抱歉，您的申请被拒绝: {reason or '无'}",
        "related_id": app.id,
        "related_type": "application"
    })
    
    return app

@router.delete("/{application_id}")
def withdraw_application(application_id: int, db: Session = Depends(get_db)):
    """撤回申请"""
    app = crud.TaskApplicationCRUD.get_by_id(db, application_id)
    if not app:
        raise HTTPException(status_code=404, detail="申请不存在")
    
    if app.status == "PENDING":
        app.status = "WITHDRAWN"
        db.commit()
    
    return {"message": "撤回成功"}
