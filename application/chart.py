from typing import List

from db.repositories.project import ProjectRepositoryImpl
from db.repositories.user import UserRepositoryImpl
from domain.models.chart.project_with_total_time import ProjectWithTotalTime
from domain.models.project.project_id import ProjectId
from domain.models.user.user_id import UserId

user_rep = UserRepositoryImpl()
project_rep = ProjectRepositoryImpl()


def get_projects_with_total_time() -> List[ProjectWithTotalTime]:
    projects_with_total_time: List[ProjectWithTotalTime] = project_rep.select_projects_with_total_time()
    return projects_with_total_time


def get_projects_with_users(project_id: ProjectId):
    return user_rep.select_projects_with_users(project_id=project_id)


def get_projects_with_users_per_month(project_id: ProjectId):
    return user_rep.select_projects_with_users_per_month(project_id=project_id)


def get_user_with_projects(user_id: UserId):
    return user_rep.select_users_with_projects(user_id=user_id)
