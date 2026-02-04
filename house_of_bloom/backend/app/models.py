from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db import Base


class Category(Base):
    __tablename__ = 'categories'

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    image = Column(String)
    product_count = Column(Integer, default=0)

    plants = relationship('Plant', back_populates='category', cascade='all, delete-orphan')


class Plant(Base):
    __tablename__ = 'plants'

    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, nullable=False, index=True)
    handle = Column(String)
    name = Column(String, nullable=False)
    description = Column(Text)
    category_id = Column(String, ForeignKey('categories.id'), index=True)
    type = Column(String)
    product_category = Column(String)
    tags = Column(String)
    price = Column(String)
    inventory = Column(Integer)
    image = Column(String)
    vendor = Column(String)
    status = Column(String)

    category = relationship('Category', back_populates='plants')


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    history = relationship('BrowsingHistory', back_populates='user', cascade='all, delete-orphan')


class BrowsingHistory(Base):
    __tablename__ = 'browsing_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    path = Column(String, nullable=False)
    referrer = Column(String)
    additional_metadata = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='history')
