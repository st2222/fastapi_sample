from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from db.setting.setting import Base


class ReportDataModel(Base):
    __tablename__ = 'reports'

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    date = Column(DateTime, nullable=False)
    comment = Column(String(1000), nullable=True)
    plan = Column(String(1000), nullable=True)

    report_detail = relationship(
        "ReportDetailDataModel", backref="reports")
