import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ModelBase(Base):
    """ModelBase"""
    __abstract__ = True
    id = Column(UUID, server_default=sa.text("gen_random_uuid()"), primary_key=True, comment="Primary Key")

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        return None


class FireBaseModelBase(Base):
    """FireBaseModelBase"""
    __abstract__ = True
    uid = Column(sa.String(255), primary_key=True, comment="uid")

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        return None
