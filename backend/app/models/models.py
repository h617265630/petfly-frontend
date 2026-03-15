"""
PetFly 数据库模型
"""
from sqlalchemy import Column, BigInteger, String, Enum, Date, DateTime, Text, DECIMAL, ForeignKey, UniqueConstraint, Index, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum

class UserRole(str, enum.Enum):
    OWNER = "OWNER"
    FLYER = "FLYER"
    MANAGER = "MANAGER"

class UserStatus(int, enum.Enum):
    DISABLED = 0
    ACTIVE = 1

class PetType(str, enum.Enum):
    DOG = "DOG"
    CAT = "CAT"
    OTHER = "OTHER"

class PetGender(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"

class TransportType(str, enum.Enum):
    CABIN = "CABIN"
    CARGO = "CARGO"
    BOTH = "BOTH"

class VisaType(str, enum.Enum):
    TOURIST = "Tourist"
    WORK = "Work"
    STUDENT = "Student"
    OTHER = "Other"

class TaskStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    OPEN = "OPEN"
    SELECTING = "SELECTING"
    CONFIRMING = "CONFIRMING"
    CONFIRMED = "CONFIRMED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class ApplicationStatus(str, enum.Enum):
    PENDING = "PENDING"
    SHORTLISTED = "SHORTLISTED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"

class ConfirmationStatus(str, enum.Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

# ============ 用户表 ============
class User(Base):
    __tablename__ = "users"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    phone = Column(String(20), nullable=False, unique=True, index=True)
    country_code = Column(String(10), default="+86")
    wechat = Column(String(100))
    role = Column(Enum(UserRole), default=UserRole.OWNER)
    name = Column(String(100))
    avatar = Column(String(500))
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 关联
    pets = relationship("Pet", back_populates="owner", cascade="all, delete-orphan")
    published_tasks = relationship("Task", back_populates="owner", foreign_keys="Task.owner_id")
    flyer_profile = relationship("FlyerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")


# ============ 培飞员详细信息表 ============
class FlyerProfile(Base):
    __tablename__ = "flyer_profiles"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # 护照信息
    passport_name = Column(String(100))
    passport_number = Column(String(50))
    passport_expiry = Column(Date)
    passport_image = Column(String(500))
    
    # 签证信息
    visa_type = Column(Enum(VisaType))
    visa_expiry = Column(Date)
    visa_image = Column(String(500))
    
    # 养宠经验
    has_pet_experience = Column(BigInteger, default=0)
    pet_experience_desc = Column(Text)
    pet_types_handled = Column(String(200))
    
    # 认证状态
    is_verified = Column(BigInteger, default=0)
    verified_at = Column(TIMESTAMP, nullable=True)
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 关联
    user = relationship("User", back_populates="flyer_profile")


# ============ 宠物表 ============
class Pet(Base):
    __tablename__ = "pets"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name = Column(String(100))
    pet_type = Column(Enum(PetType), nullable=False)
    breed = Column(String(200))
    weight = Column(DECIMAL(5, 2))
    age_months = Column(BigInteger)
    gender = Column(Enum(PetGender))
    image = Column(String(500))
    vaccination_record = Column(String(500))
    health_cert = Column(String(500))
    remark = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 关联
    owner = relationship("User", back_populates="pets")
    tasks = relationship("Task", back_populates="pet")


# ============ 任务表 ============
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    pet_id = Column(BigInteger, ForeignKey("pets.id", ondelete="SET NULL"), nullable=True)
    
    # 运输信息
    transport_type = Column(Enum(TransportType), default=TransportType.CABIN)
    from_city = Column(String(100), nullable=False)
    to_city = Column(String(100), nullable=False)
    middle_city = Column(String(100))
    
    # 时间
    travel_date = Column(Date, nullable=False, index=True)
    deadline = Column(DateTime)
    
    # 预算
    budget_min = Column(DECIMAL(10, 2))
    budget_max = Column(DECIMAL(10, 2))
    
    # 状态
    status = Column(Enum(TaskStatus), default=TaskStatus.DRAFT, index=True)
    selected_flyer_id = Column(BigInteger, nullable=True)
    confirmed_at = Column(TIMESTAMP, nullable=True)
    
    remark = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 索引
    __table_args__ = (
        Index("idx_from_to", "from_city", "to_city"),
        Index("idx_status_date", "status", "travel_date"),
    )
    
    # 关联
    owner = relationship("User", back_populates="published_tasks", foreign_keys=[owner_id])
    pet = relationship("Pet", back_populates="tasks")
    applications = relationship("TaskApplication", back_populates="task", cascade="all, delete-orphan")


# ============ 申请记录表 ============
class TaskApplication(Base):
    __tablename__ = "task_applications"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), index=True)
    flyer_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    
    # 行程信息
    from_city = Column(String(100))
    to_city = Column(String(100))
    travel_date = Column(Date)
    flight_number = Column(String(50))
    
    # 申请信息
    introduction = Column(Text)
    can_handle_pet_type = Column(String(200))
    has_experience = Column(BigInteger, default=0)
    experience_desc = Column(Text)
    expected_price = Column(DECIMAL(10, 2))
    
    # 状态
    status = Column(Enum(ApplicationStatus), default=ApplicationStatus.PENDING, index=True)
    reject_reason = Column(String(500))
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # 唯一约束
    __table_args__ = (
        UniqueConstraint("task_id", "flyer_id", name="uq_task_flyer"),
    )
    
    # 关联
    task = relationship("Task", back_populates="applications")


# ============ 管理员审核记录表 ============
class TaskConfirmation(Base):
    __tablename__ = "task_confirmations"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), unique=True)
    flyer_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    
    manager_id = Column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status = Column(Enum(ConfirmationStatus), default=ConfirmationStatus.PENDING)
    remark = Column(String(500))
    reject_reason = Column(String(500))
    reviewed_at = Column(TIMESTAMP, nullable=True)
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


# ============ 通知表 ============
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    
    type = Column(String(50), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    
    related_id = Column(BigInteger)
    related_type = Column(String(50))
    
    is_read = Column(BigInteger, default=0, index=True)
    read_at = Column(TIMESTAMP, nullable=True)
    
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    
    # 关联
    user = relationship("User")


# ============ 会话表 ============
class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), unique=True)
    owner_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    flyer_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    
    last_message = Column(String(500))
    last_message_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


# ============ 消息表 ============
class Message(Base):
    __tablename__ = "messages"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    conversation_id = Column(BigInteger, ForeignKey("conversations.id", ondelete="CASCADE"), index=True)
    sender_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    
    content = Column(Text, nullable=False)
    msg_type = Column(String(20), default="TEXT")
    is_read = Column(BigInteger, default=0)
    
    created_at = Column(TIMESTAMP, server_default=func.now())
