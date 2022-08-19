from domain.models.project.budget import Budget
from domain.models.project.other_cost import OtherCost
from domain.models.project.profit_rate import ProfitRate
from domain.models.project.project_id import ProjectId
from domain.models.project.project_name import ProjectName
from domain.models.project.status import Status
from domain.models.report_detail.hour import Hour


class ProjectWithTotalTime:
    def __init__(self, project_id: ProjectId, project_name: ProjectName, budget: Budget, other_cost: OtherCost,
                 profit_rate: ProfitRate, status: Status, total_time: Hour) -> None:
        # TODO: ここでバリデーションやルールなど書く
        if False:
            raise Exception

        self.project_id = project_id
        self.project_name = project_name
        self.budget = budget
        self.other_cost = other_cost
        self.profit_rate = profit_rate
        self.status = status
        self.total_time = total_time
