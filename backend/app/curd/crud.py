"""
PetFly CURD 操作
"""
from sqlalchemy.orm import Session
from app.models import models
from typing import List, Optional

# ============ 用户 CURD ============
class UserCRUD:
    @staticmethod
    def get_by_phone(db: Session, phone: str):
        return db.query(models.User).filter(models.User.phone == phone).first()
    
    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, user_data: dict):
        user = models.User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def update(db: Session, user: models.User, update_data: dict):
        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def delete(db: Session, user_id: int):
        user = models.UserCRUD.get_by_id(db, user_id)
        if user:
            db.delete(user)
            db.commit()
        return user

# ============ 宠物 CURD ============
class PetCRUD:
    @staticmethod
    def get_by_id(db: Session, pet_id: int):
        return db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    
    @staticmethod
    def get_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
        return db.query(models.Pet).filter(models.Pet.owner_id == owner_id).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, pet_data: dict):
        pet = models.Pet(**pet_data)
        db.add(pet)
        db.commit()
        db.refresh(pet)
        return pet
    
    @staticmethod
    def update(db: Session, pet: models.Pet, update_data: dict):
        for key, value in update_data.items():
            if value is not None:
                setattr(pet, key, value)
        db.commit()
        db.refresh(pet)
        return pet
    
    @staticmethod
    def delete(db: Session, pet_id: int):
        pet = models.PetCRUD.get_by_id(db, pet_id)
        if pet:
            db.delete(pet)
            db.commit()
        return pet

# ============ 任务 CURD ============
class TaskCRUD:
    @staticmethod
    def get_by_id(db: Session, task_id: int):
        return db.query(models.Task).filter(models.Task.id == task_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, status: Optional[str] = None):
        query = db.query(models.Task)
        if status:
            query = query.filter(models.Task.status == status)
        return query.order_by(models.Task.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_owner(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
        return db.query(models.Task).filter(
            models.Task.owner_id == owner_id
        ).order_by(models.Task.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_open_tasks(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Task).filter(
            models.Task.status == "OPEN"
        ).order_by(models.Task.travel_date.asc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, task_data: dict):
        task = models.Task(**task_data)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    @staticmethod
    def update(db: Session, task: models.Task, update_data: dict):
        for key, value in update_data.items():
            if value is not None:
                setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return task
    
    @staticmethod
    def select_flyer(db: Session, task_id: int, flyer_id: int):
        task = models.TaskCRUD.get_by_id(db, task_id)
        if task:
            task.status = "SELECTING"
            task.selected_flyer_id = flyer_id
            db.commit()
            db.refresh(task)
        return task
    
    @staticmethod
    def confirm_task(db: Session, task_id: int):
        task = models.TaskCRUD.get_by_id(db, task_id)
        if task:
            task.status = "CONFIRMED"
            db.commit()
            db.refresh(task)
        return task

# ============ 申请 CURD ============
class ApplicationCRUD:
    @staticmethod
    def get_by_id(db: Session, app_id: int):
        return db.query(models.TaskApplication).filter(models.TaskApplication.id == app_id).first()
    
    @staticmethod
    def get_by_task(db: Session, task_id: int, skip: int = 0, limit: int = 100):
        return db.query(models.TaskApplication).filter(
            models.TaskApplication.task_id == task_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_flyer(db: Session, flyer_id: int, skip: int = 0, limit: int = 100):
        return db.query(models.TaskApplication).filter(
            models.TaskApplication.flyer_id == flyer_id
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_task_and_flyer(db: Session, task_id: int, flyer_id: int):
        return db.query(models.TaskApplication).filter(
            models.TaskApplication.task_id == task_id,
            models.TaskApplication.flyer_id == flyer_id
        ).first()
    
    @staticmethod
    def create(db: Session, app_data: dict):
        app = models.TaskApplication(**app_data)
        db.add(app)
        db.commit()
        db.refresh(app)
        return app
    
    @staticmethod
    def update_status(db: Session, app_id: int, status: str, reject_reason: Optional[str] = None):
        app = models.TaskApplicationCRUD.get_by_id(db, app_id)
        if app:
            app.status = status
            if reject_reason:
                app.reject_reason = reject_reason
            db.commit()
            db.refresh(app)
        return app
    
    @staticmethod
    def delete(db: Session, app_id: int):
        app = models.TaskApplicationCRUD.get_by_id(db, app_id)
        if app:
            db.delete(app)
            db.commit()
        return app

# 使用别名
class TaskApplicationCRUD(ApplicationCRUD):
    pass

# ============ 通知 CURD ============
class NotificationCRUD:
    @staticmethod
    def get_by_id(db: Session, notif_id: int):
        return db.query(models.Notification).filter(models.Notification.id == notif_id).first()
    
    @staticmethod
    def get_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 50):
        return db.query(models.Notification).filter(
            models.Notification.user_id == user_id
        ).order_by(models.Notification.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_unread_count(db: Session, user_id: int):
        return db.query(models.Notification).filter(
            models.Notification.user_id == user_id,
            models.Notification.is_read == 0
        ).count()
    
    @staticmethod
    def create(db: Session, notif_data: dict):
        notif = models.Notification(**notif_data)
        db.add(notif)
        db.commit()
        db.refresh(notif)
        return notif
    
    @staticmethod
    def mark_as_read(db: Session, notif_id: int):
        notif = models.NotificationCRUD.get_by_id(db, notif_id)
        if notif:
            notif.is_read = 1
            from datetime import datetime
            notif.read_at = datetime.now()
            db.commit()
            db.refresh(notif)
        return notif
    
    @staticmethod
    def mark_all_as_read(db: Session, user_id: int):
        db.query(models.Notification).filter(
            models.Notification.user_id == user_id,
            models.Notification.is_read == 0
        ).update({"is_read": 1})
        db.commit()
