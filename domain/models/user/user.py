from datetime import datetime
from typing import List, Optional

from domain.models.report.report import Report
from domain.models.user.password import HashedPassword
from domain.models.date import Date
from domain.models.user.cost_per_hour import CostPerHour
from domain.models.user.image import Image
from domain.models.user.email import Email
from domain.models.user.user_name import UserName
from domain.models.user.user_id import UserId
from domain.models.user.role import Role


class User:

    def __init__(self, user_id: Optional[UserId] = None, user_name: Optional[UserName] = None,
                 email: Optional[Email] = None, image: Optional[Image] = None,
                 cost_per_hour: Optional[CostPerHour] = None,
                 created_at: Optional[datetime] = None, password: Optional[HashedPassword] = None,
                 delete_flag: Optional[bool] = None,
                 role: Optional[Role] = None,
                 reports: List[Report] = []) -> None:
        # TODO: ここでバリデーションやルールなど書く
        # if False:
        #     raise Exception

        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.image = image
        self.cost_per_hour = cost_per_hour
        self.created_at = created_at
        self.password = password
        self.delete_flag = delete_flag
        self.role = role
        self.reports = reports
