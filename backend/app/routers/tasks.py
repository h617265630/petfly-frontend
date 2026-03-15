"""
任务路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas import schemas
from app.curd import crud
from app.models import models

router = APIRouter()

@router.post("/", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """创建任务"""
    task_data = task.model_dump()
    return crud.TaskCRUD.create(db, task_data)

@router.get("/", response_model=list[schemas.TaskResponse])
def list_tasks(
    skip: int = 0, 
    limit: int = 100, 
    status: str = None,
    from_city: str = None,
    to_city: str = None,
    db: Session = Depends(get_db)
):
    """获取任务列表"""
    query = db.query(models.Task)
    
    if status:
        query = query.filter(models.Task.status == status)
    if from_city:
        query = query.filter(models.Task.from_city.contains(from_city))
    if to_city:
        query = query.filter(models.Task.to_city.contains(to_city))
    
    return query.order_by(models.Task.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/open", response_model=list[schemas.TaskResponse])
def get_open_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取开放的任务列表"""
    return crud.TaskCRUD.get_open_tasks(db, skip, limit)

@router.get("/my", response_model=list[schemas.TaskResponse])
def get_my_tasks(owner_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取我发布的任务"""
    return crud.TaskCRUD.get_by_owner(db, owner_id, skip, limit)

@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """获取任务详情"""
    task = crud.TaskCRUD.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """更新任务"""
    task = crud.TaskCRUD.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return crud.TaskCRUD.update(db, task, task_update.model_dump(exclude_unset=True))

@router.post("/{task_id}/publish", response_model=schemas.TaskResponse)
def publish_task(task_id: int, db: Session = Depends(get_db)):
    """发布任务（状态变为 OPEN）"""
    task = crud.TaskCRUD.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if task.status != "DRAFT":
        raise HTTPException(status_code=400, detail="只有草稿状态的任务可以发布")
    
    task.status = "OPEN"
    db.commit()
    db.refresh(task)
    return task

@router.post("/{task_id}/select-flyer", response_model=schemas.TaskResponse)
def select_flyer(task_id: int, flyer_id: int, db: Session = Depends(get_db)):
    """选择培飞员"""
    task = crud.TaskCRUD.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if task.status != "OPEN":
        raise HTTPException(status_code=400, detail="只有开放状态的任务可以选择培飞员")
    
    # 更新任务状态
    task.status = "SELECTING"
    task.selected_flyer_id = flyer_id
    db.commit()
    db.refresh(task)
    
    # 更新被选中的申请状态
    application = crud.TaskApplicationCRUD.get_by_task_and_flyer(db, task_id, flyer_id)
    if application:
        application.status = "SHORTLISTED"
        db.commit()
    
    # 通知培飞员
    notification = crud.NotificationCRUD.create(db, {
        "user_id": flyer_id,
        "type": "SELECTED",
        "title": "您被选中了！",
        "content": f"任务 #{task_id} 的主人选择了您",
        "related_id": task_id,
        "related_type": "task"
    })
    
    return task

@router.post("/{task_id}/request-confirm", response_model=schemas.TaskResponse)
def request_confirmation(task_id: int, db: Session = Depends(get_db)):
    """请求管理员确认"""
    task = crud.TaskCRUD.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if task.status != "SELECTING":
        raise HTTPException(status_code=400, detail="只有选择中状态的任务可以请求确认")
    
    task.status = "CONFIRMING"
    db.commit()
    db.refresh(task)
    
    # 通知管理员
    managers = db.query(models.User).filter(models.User.role == "MANAGER").all()
    for manager in managers:
        crud.NotificationCRUD.create(db, {
            "user_id": manager.id,
            "type": "CONFIRM_REQUEST",
            "title": "有任务待确认",
            "content": f"任务 #{task_id} 需要管理员确认",
            "related_id": task_id,
            "related_type": "task"
        })
    
    return task

@router.post("/{task_id}/confirm", response_model=schemas.TaskResponse)
def confirm_task(task_id: int, manager_id: int, db: Session = Depends(get_db)):
    """管理员确认任务"""
    task = crud.TaskCRUD.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if task.status != "CONFIRMING":
        raise HTTPException(status_code=400, detail="只有确认中的任务可以确认")
    
    # 创建确认记录
    confirmation = crud.models.TaskConfirmation(
        task_id=task_id,
        flyer_id=task.selected_flyer_id,
        manager_id=manager_id,
        status="APPROVED"
    )
    db.add(confirmation)
    
    # 更新任务状态
    task.status = "CONFIRMED"
    from datetime import datetime
    task.confirmed_at = datetime.now()
    db.commit()
    db.refresh(task)
    
    # 通知用户
    crud.NotificationCRUD.create(db, {
        "user_id": task.owner_id,
        "type": "CONFIRMED",
        "title": "任务已确认",
        "content": f"任务 #{task_id} 已通过管理员确认",
        "related_id": task_id,
        "related_type": "task"
    })
    
    if task.selected_flyer_id:
        crud.NotificationCRUD.create(db, {
            "user_id": task.selected_flyer_id,
            "type": "CONFIRMED",
            "title": "任务已确认",
            "content": f"您已被确认为任务 #{task_id} 的陪飞员",
            "related_id": task_id,
            "related_type": "task"
        })
    
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """删除任务"""
    task = crud.TaskCRUD.get_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    
    db.delete(task)
    db.commit()
    return {"message": "删除成功"}
