from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from db.setting.setting import Base
from db.models.report_detail import ReportDetailDataModel


class ProjectDataModel(Base):

    __tablename__ = 'projects'
    project_id = Column(Integer, primary_key=True, autoincrement=True)
    project_name = Column(String(100), nullable=False)
    budget = Column(Integer, nullable=False)
    profit_rate = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    other_cost = Column(Integer, nullable=False)

    report_detail = relationship("ReportDetailDataModel", backref="projects")


