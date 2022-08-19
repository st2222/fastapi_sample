from domain.models.report.report_id import ReportId
from typing import List
from db.repositories.report import ReportRepositoryImpl
from domain.models.report.report import Report
from domain.services.report import exists
from exception.exception import NotFoundException

rep = ReportRepositoryImpl()


def register(report: Report) -> None:
    rep.insert(report)


def select_all_reports() -> List[Report]:
    return rep.select()


def find_report(report_id: ReportId) -> Report:
    report: Report = rep.find_report(report_id)
    if not exists(report):
        raise NotFoundException(f'{report_id.value} is not found')
    return report


def update_report(report_id: ReportId, body) -> None:
    report: Report = rep.find_report(report_id)
    if not exists(report):
        raise NotFoundException(f'{report_id.value} is not found')
    rep.update_report(report_id, body)
