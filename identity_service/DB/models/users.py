from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey, Integer, ARRAY, func, Index
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

import uuid
from identity_service.DB.database import Base
from identity_service.DB.enums import UserGender, UserRole, AuthProvider



class User(Base):
    __tablename__ = "users"

    user_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(String, nullable=False)  
    email = Column(String, nullable=False, unique=True)
    gender = Column(Enum(UserGender), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
