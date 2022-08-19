from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy import Column, Integer, String, DateTime

from db.setting.setting import Base
from db.models.report import ReportDataModel


class UserDataModel(Base):
    __tablename__ = 'users'

    user_id = Column(Integer(), primary_key=True, autoincrement=True)
    user_name = Column(String(100), nullable=False)
    image = Column(String(255), nullable=False)
    cost_per_hour = Column(Integer(), nullable=False)

    email = Column(String(255), primary_key=True)
    password = Column(String(255), nullable=False)
    role = Column(Integer(), nullable=False)
    delete_flag = Column(Boolean(False), nullable=False)
    created_at = Column(DateTime(), nullable=False)

    # 文字列だがimportしないとErrorになる
    reports = relationship("ReportDataModel", backref="users")
