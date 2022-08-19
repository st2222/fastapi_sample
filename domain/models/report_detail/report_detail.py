from typing import List

from domain.models.project.project_id import ProjectId
from domain.models.report.report_id import ReportId

from domain.models.date import Date
from domain.models.report.comment import Comment
from domain.models.report.plan import Plan
from domain.models.report_detail.hour import Hour
from domain.models.report_detail.report_detail_id import ReportDetailId
from domain.models.user.user_id import UserId


class ReportDetail:
    def __init__(self, report_detail_id: ReportDetailId, report_id: ReportId, project_id: ProjectId,
                 hour: Hour) -> None:
        # TODO: ここでバリデーションやルールなど書く
        if False:
            raise Exception

        self.report_detail_id = report_detail_id
        self.report_id = report_id
        self.project_id = project_id
        self.hour = hour
