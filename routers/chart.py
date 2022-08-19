from typing import List

from fastapi import APIRouter, Query, Depends
from pydantic import BaseModel

from application.chart import get_projects_with_total_time, get_projects_with_users, get_projects_with_users_per_month, \
    get_user_with_projects
from domain.models.chart.project_with_total_time import ProjectWithTotalTime
from domain.models.project.project_id import ProjectId
from domain.models.user.user_id import UserId
from routers.auth import oauth2_scheme

router = APIRouter()


class ProjectWithTotalTimeModel(BaseModel):
    project_id: int
    project_name: str
    budget: int
    other_cost: int
    profit_rate: int
    status: int
    total_time: int


class ProjectWithUserModel(BaseModel):
    project_id: int
    user_id: int
    user_name: str
    role: int
    cost_per_hour: int
    total_time: int


class ProjectWithUserPerMonthModel(BaseModel):
    month: str
    project_id: int
    user_id: int
    user_name: str
    role: int
    cost_per_hour: int
    total_time: int


class UserWithProject(BaseModel):
    month: str
    project_id: int
    project_name: str
    user_id: int
    user_name: str
    role: int
    cost_per_hour: int
    total_time: int


@router.get("/chart")
def get_projects_chart(token=Depends(oauth2_scheme)):
    project_with_total_time_list: List[ProjectWithTotalTime] = get_projects_with_total_time()

    return list(
        map(lambda x: ProjectWithTotalTimeModel(project_id=x.project_id.value,
                                                project_name=x.project_name.value,
                                                budget=x.budget.value,
                                                other_cost=x.other_cost.value,
                                                profit_rate=x.profit_rate.value,
                                                status=x.status.value,
                                                total_time=x.total_time.value),
            project_with_total_time_list))


@router.get("/chart/projects")
def get_project_chart(project_id: int = Query(None), token=Depends(oauth2_scheme)):
    return list(
        map(lambda x: ProjectWithUserModel(project_id=x.project_id.value,
                                           user_id=x.user_id.value,
                                           user_name=x.user_name.value,
                                           role=x.role.value,
                                           cost_per_hour=x.cost_per_hour.value,
                                           total_time=x.total_time.value),
            get_projects_with_users(ProjectId(project_id))))


@router.get("/chart/projects/transition")
def get_project_transition_chart(project_id: int = Query(None), token=Depends(oauth2_scheme)):
    return list(
        map(lambda x: ProjectWithUserPerMonthModel(month=x.month.value,
                                                   project_id=x.project_id.value,
                                                   user_id=x.user_id.value,
                                                   user_name=x.user_name.value,
                                                   role=x.role.value,
                                                   cost_per_hour=x.cost_per_hour.value,
                                                   total_time=x.total_time.value),
            get_projects_with_users_per_month(ProjectId(project_id))))


@router.get("/chart/users")
def get_users_chart(user_id: int = Query(None), token=Depends(oauth2_scheme)):
    return list(
        map(lambda x: UserWithProject(month=x.month.value,
                                      project_id=x.project_id.value,
                                      project_name=x.project_name.value,
                                      user_id=x.user_id.value,
                                      user_name=x.user_name.value,
                                      role=x.role.value,
                                      cost_per_hour=x.cost_per_hour.value,
                                      total_time=x.total_time.value),
            get_user_with_projects(UserId(user_id))))
