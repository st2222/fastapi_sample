from abc import ABC, abstractmethod
from typing import Optional, Dict

from sqlalchemy import false

from db.models.report_detail import ReportDetailDataModel
from domain.models.date import Date
from domain.models.project.project_id import ProjectId
from domain.models.report.comment import Comment
from domain.models.report.plan import Plan
from domain.models.report.report_id import ReportId
from typing import List
from db.setting.setting import session
from db.models.report import ReportDataModel
from domain.models.report.report import Report
from domain.models.report_detail.hour import Hour
from domain.models.report_detail.report_detail import ReportDetail
from domain.models.report_detail.report_detail_id import ReportDetailId
from domain.models.user.user_id import UserId


class ReportRepository(ABC):

    @abstractmethod
    def insert(self, report: Report) -> None:
        pass

    @abstractmethod
    def select(self) -> List[Report]:
        pass

    @abstractmethod
    def find_report(self, report: Report) -> Optional[Report]:
        pass

    @abstractmethod
    def update_report(self, report_id: ReportId, body: Dict) -> None:
        pass

    @abstractmethod
    def delete_report(self, report: Report) -> None:
        pass

    # @abstractmethod
    # def __to_report(self, report_data_model: ReportDataModel) -> Report:
    #     pass
    #
    # @abstractmethod
    # def __to_report_data_model(self, report: Report) -> ReportDataModel:
    #     pass


class ReportRepositoryImpl(ReportRepository):

    def insert(self, report: Report) -> None:
        report_data_model: ReportDataModel = to_report_data_model(report)

        try:
            session.add(report_data_model)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        session.close()

    def select(self) -> List[Report]:
        return list(map(lambda x: to_report(x),
                        session.query(ReportDataModel).all()))

    def find_report(self, report_id: ReportId) -> Optional[Report]:
        report_data_model = session.query(ReportDataModel).filter(ReportDataModel.report_id == report_id.value).first()
        if report_data_model is None:
            return None
        return to_report(report_data_model)

    def update_report(self, report_id: ReportId, body: Dict) -> None:
        try:
            report_data_model: ReportDataModel = session.query(ReportDataModel).filter(
                ReportDataModel.report_id == report_id.value).first()
            for key, value in body.items():
                print(setattr(report_data_model, key, value))
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        session.close()

    def delete_report(self, report: Report) -> None:
        try:
            report_data_model: ReportDataModel = session.query(ReportDataModel).filter(
                ReportDataModel.report_id == report.report_id.value).first()
            report_data_model.delete_flag = True
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        session.close()


def to_report_data_model(report: Report) -> ReportDataModel:
    report_data_model = ReportDataModel()
    # report_data_model.report_id = report.report_id.value
    report_data_model.user_id = report.user_id.value
    report_data_model.date = report.date
    report_data_model.comment = report.comment.value
    report_data_model.plan = report.plan.value
    report_data_model.report_detail = list(
        map(lambda x: ReportDetailDataModel(report_id=x.report_id.value, project_id=x.project_id.value,
                                            hour=x.hour.value), report.report_detail))

    return report_data_model


def to_report(report_data_model: ReportDataModel) -> Report:
    report = Report(report_id=ReportId(report_data_model.report_id),
                    user_id=UserId(report_data_model.user_id),
                    date=report_data_model.date,
                    comment=Comment(report_data_model.comment),
                    plan=Plan(report_data_model.plan),
                    report_detail=list(
                        map(lambda x: ReportDetail(report_detail_id=ReportDetailId(x.report_detail_id),
                                                   report_id=ReportId(x.report_id),
                                                   project_id=ProjectId(x.project_id), hour=Hour(x.hour)),
                            report_data_model.report_detail)))

    return report
