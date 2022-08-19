from abc import ABC, abstractmethod
from typing import Optional, Dict

import sqlalchemy
from sqlalchemy import false, func, select
from sqlalchemy.orm import DeclarativeMeta

from db.models.project import ProjectDataModel
from db.models.report import ReportDataModel
from db.models.report_detail import ReportDetailDataModel
from db.repositories.report import to_report
from domain.models.chart.project_with_users import ProjectWithUser
from domain.models.chart.project_with_users_per_month import ProjectWithUserPerMonth
from domain.models.chart.user_with_project import UserWithProject
from domain.models.date import Date
from domain.models.project.project_id import ProjectId
from domain.models.project.project_name import ProjectName
from domain.models.report_detail.hour import Hour
from domain.models.user.cost_per_hour import CostPerHour
from domain.models.user.email import Email
from domain.models.user.image import Image
from domain.models.user.password import HashedPassword
from domain.models.user.role import Role
from domain.models.user.user_id import UserId
from typing import List
from db.setting.setting import session
from db.models.user import UserDataModel
from domain.models.user.user import User
from domain.models.user.user_name import UserName


class UserRepository(ABC):

    @abstractmethod
    def insert(self, user: User) -> None:
        pass

    @abstractmethod
    def select(self) -> List[User]:
        pass

    @abstractmethod
    def find_user_by_id(self, user_id: UserId) -> Optional[User]:
        pass

    @abstractmethod
    def find_user_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    def update_user(self, user_id: UserId, body: Dict) -> None:
        pass

    @abstractmethod
    def delete_user(self, user: User) -> None:
        pass

    @abstractmethod
    def select_projects_with_users(self, project_id: ProjectId) -> List:
        pass

    @abstractmethod
    def select_projects_with_users_per_month(self, project_id: ProjectId):
        pass

    @abstractmethod
    def select_users_with_projects(self, project_id: ProjectId):
        pass


class UserRepositoryImpl(UserRepository):

    def insert(self, user: User) -> None:
        user_data_model: UserDataModel = to_user_data_model(user)

        try:
            session.add(user_data_model)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        session.close()

    def select(self) -> List[User]:
        return list(map(lambda x: to_user(x),
                        session.query(
                            UserDataModel,
                        ).filter(
                            UserDataModel.delete_flag == false()
                        ).all()))

    def find_user_by_id(self, user_id: UserId) -> Optional[User]:
        user_data_model = session.query(UserDataModel).filter(UserDataModel.user_id == user_id.value).first()
        return to_user(user_data_model)

    def find_user_by_email(self, email: Email) -> Optional[User]:
        user_data_model = session.query(UserDataModel).filter(UserDataModel.email == email.value).first()
        return to_user(user_data_model)

    def update_user(self, user_id: UserId, body: Dict) -> None:
        try:
            user_data_model: UserDataModel = session.query(UserDataModel).filter(
                UserDataModel.user_id == user_id.value).first()
            for key, value in body.items():
                setattr(user_data_model, key, value)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        session.close()

    def delete_user(self, user: User) -> None:
        try:
            user_data_model: UserDataModel = session.query(UserDataModel).filter(
                UserDataModel.user_id == user.user_id.value).first()
            user_data_model.delete_flag = True
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        session.close()

    def select_projects_with_users(self, project_id: ProjectId) -> List:
        """
        SELECT
            u.user_id, u.user_name, u.role, rd.project_id, SUM(rd.hour)
        FROM
            nippo.users AS u
        INNER JOIN
            nippo.reports AS r ON u.user_id = r.user_id
        INNER JOIN
            nippo.report_detail rd ON r.report_id = rd.report_id
        WHERE
            rd.project_id = 1 AND u.delete_flag = 0
        GROUP BY u.user_id , u.user_name;
        """
        projects_data_model_with_users: List = session.query(
            UserDataModel.user_id,
            UserDataModel.user_name,
            UserDataModel.role,
            UserDataModel.cost_per_hour,
            ReportDetailDataModel.project_id,
            func.sum(ReportDetailDataModel.hour).label("total_time")
        ).join(
            ReportDataModel,
            UserDataModel.user_id == ReportDataModel.user_id
        ).join(
            ReportDetailDataModel, ReportDataModel.report_id == ReportDetailDataModel.report_id
        ).filter(
            ReportDetailDataModel.project_id == project_id.value,
            UserDataModel.delete_flag == false()
        ).group_by(
            UserDataModel.user_id, UserDataModel.user_name, UserDataModel.role, UserDataModel.cost_per_hour,
            ReportDetailDataModel.project_id
        ).all()

        projects_with_users: List[ProjectWithUser] = list(
            map(lambda x: ProjectWithUser(project_id=ProjectId(x['project_id']),
                                          user_id=UserId(x['user_id']),
                                          user_name=UserName(x['user_name']), role=Role(x['role']),
                                          cost_per_hour=CostPerHour(x['cost_per_hour']),
                                          total_time=Hour(x['total_time'])),
                projects_data_model_with_users))

        return projects_with_users

    def select_projects_with_users_per_month(self, project_id: ProjectId):
        """
        SELECT
            DATE_FORMAT(date, '%Y-%m') AS formatted_date,
            u.user_id,
            u.user_name,
            u.role,
            u.cost_per_hour,
            SUM(rd.hour)
        FROM
            nippo.users AS u
                INNER JOIN
            nippo.reports AS r ON u.user_id = r.user_id
                INNER JOIN
            nippo.report_detail rd ON r.report_id = rd.report_id
        WHERE
            rd.project_id = 1 AND u.delete_flag = 0
        GROUP BY formatted_date , u.user_id;
        """
        month = func.date_format(ReportDataModel.date, '%Y-%m').label('month')
        projects_data_model_with_users_per_month: List = session.query(
            month,
            UserDataModel.user_id,
            UserDataModel.user_name,
            UserDataModel.role,
            UserDataModel.cost_per_hour,
            ReportDetailDataModel.project_id,
            func.sum(ReportDetailDataModel.hour).label("total_time")
        ).join(
            ReportDataModel,
            UserDataModel.user_id == ReportDataModel.user_id
        ).join(
            ReportDetailDataModel, ReportDataModel.report_id == ReportDetailDataModel.report_id
        ).filter(
            ReportDetailDataModel.project_id == project_id.value,
            UserDataModel.delete_flag == false()
        ).group_by(
            month, UserDataModel.user_id, UserDataModel.user_name, UserDataModel.role, UserDataModel.cost_per_hour,
            ReportDetailDataModel.project_id
        ).all()

        projects_with_users_per_month: List[ProjectWithUserPerMonth] = list(
            map(lambda x: ProjectWithUserPerMonth(month=Date(x['month']),
                                                  project_id=ProjectId(x['project_id']),
                                                  user_id=UserId(x['user_id']),
                                                  user_name=UserName(x['user_name']), role=Role(x['role']),
                                                  cost_per_hour=CostPerHour(x['cost_per_hour']),
                                                  total_time=Hour(x['total_time'])),
                projects_data_model_with_users_per_month))

        return projects_with_users_per_month

    def select_users_with_projects(self, user_id: UserId):
        """
        SELECT
            DATE_FORMAT(date, '%Y-%m') AS formatted_date,
            u.user_id,
            u.user_name,
            u.role,
            u.cost_per_hour,
            SUM(rd.hour),
            rd.project_id,
            p.project_name
        FROM
            nippo.users AS u
                INNER JOIN
            nippo.reports AS r ON u.user_id = r.user_id
                INNER JOIN
            nippo.report_detail rd ON r.report_id = rd.report_id
                INNER JOIN
            nippo.projects p ON rd.project_id = p.project_id
        WHERE
            u.user_id = 1 AND u.delete_flag = 0
        GROUP BY formatted_date , u.user_id , rd.project_id , p.project_name;"""
        month = func.date_format(ReportDataModel.date, '%Y-%m').label('month')
        total_time = func.sum(ReportDetailDataModel.hour).label("total_time")
        users_data_model_with_projects: List = session.query(
            month,
            UserDataModel.user_id,
            UserDataModel.user_name,
            UserDataModel.role,
            UserDataModel.cost_per_hour,
            ReportDetailDataModel.project_id,
            total_time,
            ProjectDataModel.project_name
        ).join(
            ReportDataModel, UserDataModel.user_id == ReportDataModel.user_id
        ).join(
            ReportDetailDataModel, ReportDataModel.report_id == ReportDetailDataModel.report_id
        ).join(
            ProjectDataModel, ReportDetailDataModel.project_id == ProjectDataModel.project_id
        ).filter(
            UserDataModel.user_id == user_id.value,
            UserDataModel.delete_flag == false()
        ).group_by(
            month, UserDataModel.user_id, UserDataModel.user_name, UserDataModel.role, UserDataModel.cost_per_hour,
            ReportDetailDataModel.project_id, ProjectDataModel.project_name
        ).all()

        projects_with_users_per_month: List[UserWithProject] = list(
            map(lambda x: UserWithProject(month=Date(x['month']),
                                          project_id=ProjectId(x['project_id']),
                                          project_name=ProjectName(x['project_name']),
                                          user_id=UserId(x['user_id']),
                                          user_name=UserName(x['user_name']), role=Role(x['role']),
                                          cost_per_hour=CostPerHour(x['cost_per_hour']),
                                          total_time=Hour(x['total_time'])),
                users_data_model_with_projects))

        return projects_with_users_per_month


def to_user_data_model(user: User) -> UserDataModel:
    user_data_model = UserDataModel()
    # user_data_model.user_id = user.user_id
    user_data_model.user_name = user.user_name.value
    user_data_model.email = user.email.value
    user_data_model.image = user.image.value
    user_data_model.password = user.password.value
    user_data_model.role = user.role.value
    user_data_model.delete_flag = user.delete_flag
    user_data_model.cost_per_hour = user.cost_per_hour.value
    user_data_model.created_at = user.created_at

    return user_data_model


def to_user(user_data_model: UserDataModel) -> Optional[User]:
    # print(user_data_model.user_id)
    if user_data_model is None:
        return None
    user = User(user_id=UserId(user_data_model.user_id), user_name=UserName(user_data_model.user_name),
                email=Email(user_data_model.email), image=Image(user_data_model.image),
                password=HashedPassword(user_data_model.password),
                role=Role(user_data_model.role), delete_flag=user_data_model.delete_flag,
                created_at=user_data_model.created_at,
                cost_per_hour=CostPerHour(user_data_model.cost_per_hour))
    # d, a = {}, []
    # for rowproxy in resultproxy:
    #     # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
    #     for column, value in rowproxy.items():
    #         # build up the dictionary
    #         d = {**d, **{column: value}}
    #     a.append(d)
    #
    return user
