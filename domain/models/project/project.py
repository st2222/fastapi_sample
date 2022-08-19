from typing import List

from domain.models.project.budget import Budget
from domain.models.project.other_cost import OtherCost
from domain.models.project.profit_rate import ProfitRate
from domain.models.project.project_id import ProjectId
from domain.models.project.project_name import ProjectName
from domain.models.project.status import Status
from domain.models.report_detail.report_detail import ReportDetail


class Project:
    def __init__(self, project_id: ProjectId, project_name: ProjectName, budget: Budget, profit_rate: ProfitRate,
                 status: Status,other_cost: OtherCost, report_detail: List[ReportDetail] = []) -> None:

        self.project_id = project_id
        self.project_name = project_name
        self.budget = budget
        self.profit_rate = profit_rate
        self.status = status
        self.other_cost = other_cost

        self.report_detail = report_detail
