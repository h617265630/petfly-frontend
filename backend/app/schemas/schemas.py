"""
PetFly Pydantic Schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

# ============ 用户 Schema ============
class UserBase(BaseModel):
    phone: str
    country_code: Optional[str] = "+86"
    wechat: Optional[str] = None
    name: Optional[str] = None
    avatar: Optional[str] = None

class UserCreate(UserBase):
    role: Optional[str] = "OWNER"

class UserUpdate(BaseModel):
    name: Optional[str] = None
    avatar: Optional[str] = None
    wechat: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: str
    status: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============ 培飞员信息 Schema ============
class FlyerProfileBase(BaseModel):
    passport_name: Optional[str] = None
    passport_number: Optional[str] = None
    passport_expiry: Optional[date] = None
    visa_type: Optional[str] = None
    visa_expiry: Optional[date] = None
    has_pet_experience: Optional[int] = 0
    pet_experience_desc: Optional[str] = None
    pet_types_handled: Optional[str] = None

class FlyerProfileCreate(FlyerProfileBase):
    pass

class FlyerProfileUpdate(FlyerProfileBase):
    pass

class FlyerProfileResponse(FlyerProfileBase):
    id: int
    user_id: int
    is_verified: int
    verified_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ============ 宠物 Schema ============
class PetBase(BaseModel):
    name: Optional[str] = None
    pet_type: str
    breed: Optional[str] = None
    weight: Optional[float] = None
    age_months: Optional[int] = None
    gender: Optional[str] = None
    image: Optional[str] = None
    vaccination_record: Optional[str] = None
    health_cert: Optional[str] = None
    remark: Optional[str] = None

class PetCreate(PetBase):
    owner_id: int

class PetUpdate(BaseModel):
    name: Optional[str] = None
    breed: Optional[str] = None
    weight: Optional[float] = None
    age_months: Optional[int] = None
    gender: Optional[str] = None
    image: Optional[str] = None
    remark: Optional[str] = None

class PetResponse(PetBase):
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============ 任务 Schema ============
class TaskBase(BaseModel):
    from_city: str
    to_city: str
    middle_city: Optional[str] = None
    travel_date: date
    deadline: Optional[datetime] = None
    transport_type: Optional[str] = "CABIN"
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    remark: Optional[str] = None

class TaskCreate(TaskBase):
    owner_id: int
    pet_id: Optional[int] = None
    status: Optional[str] = "DRAFT"

class TaskUpdate(BaseModel):
    from_city: Optional[str] = None
    to_city: Optional[str] = None
    travel_date: Optional[date] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    status: Optional[str] = None
    remark: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    owner_id: int
    pet_id: Optional[int] = None
    status: str
    selected_flyer_id: Optional[int] = None
    confirmed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ============ 申请 Schema ============
class ApplicationBase(BaseModel):
    from_city: Optional[str] = None
    to_city: Optional[str] = None
    travel_date: Optional[date] = None
    flight_number: Optional[str] = None
    introduction: Optional[str] = None
    can_handle_pet_type: Optional[str] = None
    has_experience: Optional[int] = 0
    experience_desc: Optional[str] = None
    expected_price: Optional[float] = None

class ApplicationCreate(ApplicationBase):
    task_id: int
    flyer_id: int

class ApplicationUpdate(BaseModel):
    introduction: Optional[str] = None
    expected_price: Optional[float] = None
    status: Optional[str] = None

class ApplicationResponse(ApplicationBase):
    id: int
    task_id: int
    flyer_id: int
    status: str
    reject_reason: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============ 审核 Schema ============
class ConfirmationBase(BaseModel):
    remark: Optional[str] = None

class ConfirmationCreate(ConfirmationBase):
    task_id: int
    flyer_id: int

class ConfirmationUpdate(BaseModel):
    status: Optional[str] = None
    remark: Optional[str] = None
    reject_reason: Optional[str] = None

class ConfirmationResponse(ConfirmationBase):
    id: int
    task_id: int
    flyer_id: int
    manager_id: Optional[int] = None
    status: str
    reject_reason: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ============ 通知 Schema ============
class NotificationBase(BaseModel):
    type: str
    title: str
    content: Optional[str] = None
    related_id: Optional[int] = None
    related_type: Optional[str] = None

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: int
    read_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============ 消息 Schema ============
class MessageBase(BaseModel):
    content: str
    msg_type: Optional[str] = "TEXT"

class MessageCreate(MessageBase):
    conversation_id: int
    sender_id: int

class MessageResponse(MessageBase):
    id: int
    conversation_id: int
    sender_id: int
    is_read: int
    created_at: datetime
    
    class Config:
        from_attributes = True
