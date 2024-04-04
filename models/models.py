from email.policy import default
from enum import unique
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, JSON, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID, base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime

from sqlalchemy.sql.expression import false
# from configs import Configuration
from models import Base, engine
import bcrypt
import uuid

Base = declarative_base(bind=engine)



class User(Base):

    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    username = Column(String(100), unique=True)
    firstname = Column(String(100))
    lastname = Column(String(100))
    email = Column(String(200), unique=True)
    password = Column(LargeBinary)
    mobile_no = Column(String(20))
    probile_url = Column(String)
    is_deleted  = Column(Boolean)
    is_active = Column(Boolean)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))

    def hash_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))
        

    def verify_password(self, password):
        if bcrypt.checkpw(password.encode('utf-8'), self.password):
            return True
        else:
            return False



class User_social_media(Base): 

    __tablename__ = "socialmedia"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    project_uuid = Column(UUID(as_uuid=True), ForeignKey('projects.uuid'))
    page_id = Column(String)
    profile_pic = Column(String)
    cover_pic = Column(String)
    sm_platform = Column(String)
    sm_access_token = Column(String)
    username = Column(String)
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))


class Post(Base):

    __tablename__ = "post"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    status = Column(String)
    title = Column(String)
    upload_url = Column(String)
    platform_id = Column(String)
    platform = Column(String)
    description = Column(String)
    date_publish = Column(DateTime)
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    expiry_at = Column(DateTime)
    project_uuid = Column(UUID(as_uuid=True), ForeignKey('projects.uuid'))
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    create_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))

class attachments(Base):

    __tablename__ = "attachments"
    
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    type = Column(String)
    url = Column(String)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    project_uuid = Column(UUID(as_uuid=True), ForeignKey('projects.uuid'))
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    create_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))


class sm_audit(Base):

    __tablename__ = "sm_audit"
    
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    username = Column(String)
    platform = Column(String)
    is_active = Column(Boolean, default=False)
    is_deleted = Column(Boolean, default=False)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    post_uuid = Column(UUID(as_uuid=True), ForeignKey('post.uuid'))
    create_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))

class project(Base):

    __tablename__ = "projects"
    
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    project_name  = Column(String)
    logo = Column(String)
    product_uuid = Column(UUID(as_uuid=True), ForeignKey('product.uuid'))
    is_deleted = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    platform = Column(String)
    create_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))

class upload(Base):

    __tablename__ = "uploads"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    uploads_uuid = Column(UUID(as_uuid=True), ForeignKey('projects.uuid'))
    uploads_url = Column(String)
    is_deleted = Column(Boolean,default=False)
    is_active = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))

class organisation(Base):

    __tablename__ = "organisation"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    organisation_name = Column(String)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    logo_url = Column(String)
    is_deleted = Column(Boolean,default=False)
    is_active = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))


class brand(Base):

    __tablename__ = "brand"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    brand_name = Column(String)
    brand_type = Column(String)
    organisation_uuid = Column(UUID(as_uuid=True), ForeignKey('organisation.uuid'))
    logo_url = Column(String)
    is_deleted = Column(Boolean,default=False)
    is_active = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))


class Product(Base):

    __tablename__ = "product"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    product_name = Column(String)
    product_type = Column(String)
    brand_uuid = Column(UUID(as_uuid=True), ForeignKey('brand.uuid'))
    logo_url = Column(String)
    is_deleted = Column(Boolean,default=False)
    is_active = Column(Boolean, default=True)
    create_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.uuid'))