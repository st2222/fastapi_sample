from datetime import datetime
from typing import List

from domain.models.report.report_id import ReportId

from domain.models.date import Date
from domain.models.report.comment import Comment
from domain.models.report.plan import Plan
from domain.models.report_detail.report_detail import ReportDetail
from domain.models.user.user_id import UserId


class Report:
    def __init__(self, report_id: ReportId, user_id: UserId, date: datetime, comment: Comment, plan: Plan,
                 report_detail: List[ReportDetail]) -> None:

        self.report_id = report_id
        self.user_id = user_id
        self.date = date
        self.comment = comment
        self.plan = plan
        self.report_detail = report_detail
