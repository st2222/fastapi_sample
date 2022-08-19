from domain.models.date import Date
from domain.models.project.budget import Budget
from domain.models.project.other_cost import OtherCost
from domain.models.project.profit_rate import ProfitRate
from domain.models.project.project_id import ProjectId
from domain.models.project.project_name import ProjectName
from domain.models.project.status import Status
from domain.models.report_detail.hour import Hour
from domain.models.user.role import Role
from domain.models.user.user_id import UserId
from domain.models.user.user_name import UserName


class UserWithProject:
    def __init__(self, month: Date, project_id: ProjectId, user_id: UserId, user_name: UserName, role: Role,
                 cost_per_hour, total_time: Hour, project_name: ProjectName) -> None:
        # TODO: ここでバリデーションやルールなど書く
        if False:
            raise Exception

        self.month = month
        self.project_id = project_id
        self.user_id = user_id
        self.user_name = user_name
        self.role = role
        self.cost_per_hour = cost_per_hour
        self.total_time = total_time
        self.project_name = project_name
