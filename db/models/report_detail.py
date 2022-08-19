from sqlalchemy import Column, Integer, ForeignKey

from db.setting.setting import Base


class ReportDetailDataModel(Base):
    __tablename__ = 'report_detail'
    report_detail_id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(Integer, ForeignKey('reports.report_id'))
    project_id = Column(Integer, ForeignKey('projects.project_id'))
    hour = Column(Integer, nullable=False)
