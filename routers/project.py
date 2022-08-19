from http import HTTPStatus

from starlette.responses import Response

from domain.models.project.budget import Budget
from domain.models.project.other_cost import OtherCost
from domain.models.project.profit_rate import ProfitRate
from domain.models.project.project_id import ProjectId
from domain.models.project.project_name import ProjectName
from pydantic import BaseModel
from typing import Dict, Optional, List
from application.project import register, select_all_projects, find_project, update_project
from domain.models.project.project import Project
from fastapi import APIRouter, HTTPException, Depends

from domain.models.project.status import Status
from domain.models.report.report_id import ReportId
from domain.models.report_detail.hour import Hour
from domain.models.report_detail.report_detail import ReportDetail
from domain.models.report_detail.report_detail_id import ReportDetailId
from exception.exception import NotFoundException
from routers.auth import oauth2_scheme
from routers.report import ReportDetailModel

router = APIRouter()


class ProjectModel(BaseModel):
    project_id: Optional[int] = None
    project_name: Optional[str] = None
    budget: Optional[int] = None
    status: Optional[int] = None
    other_cost: Optional[int] = None
    profit_rate: Optional[int] = None
    report_detail: List[ReportDetailModel] = []

    def to_project(self) -> Project:
        return Project(project_id=ProjectId(self.project_id), project_name=ProjectName(self.project_name),
                       budget=Budget(self.budget), status=Status(self.status), other_cost=OtherCost(self.other_cost),
                       profit_rate=ProfitRate(self.profit_rate),
                       report_detail=list(
                           map(lambda x: ReportDetail(report_detail_id=ReportDetailId(x.report_detail_id),
                                                      report_id=ReportId(x.report_id),
                                                      project_id=ProjectId(self.project_id), hour=Hour(x.hour)),
                               self.report_detail)))


@router.post('/projects')
def create_project(project_model: ProjectModel, token=Depends(oauth2_scheme)) -> Response:
    register(project_model.to_project())
    # return {"message": 'ok'}
    return Response(status_code=HTTPStatus.OK.value)


@router.get('/projects')
def get_projects(token=Depends(oauth2_scheme)) -> Dict:
    return {"data": list(
        map(lambda x: ProjectModel(project_id=x.project_id.value, project_name=x.project_name.value,
                                   budget=x.budget.value, status=x.status.value, other_cost=x.other_cost.value,
                                   profit_rate=x.profit_rate.value, ), select_all_projects()))}


@router.get('/projects/{project_id}')
def get_project_by_id(project_id: int, token=Depends(oauth2_scheme)) -> Dict:
    try:
        project: Project = find_project(ProjectId(project_id))
    except NotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.args)

    return {"data": project}


@router.patch('/projects/{project_id}')
def update_project_by_id(project_id: int, project_model: ProjectModel, token=Depends(oauth2_scheme)) -> Response:
    try:
        update_project(ProjectId(project_id), project_model.dict(exclude_unset=True))
    except NotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.args)

    return Response(status_code=HTTPStatus.OK.value)

# @router.delete('/projects/{project_id}', status_code=HTTPStatus.NO_CONTENT)
# def delete_project_by_id(project_id: int) -> Response:
#     try:
#         delete_project(ProjectId(project_id))
#     except NotFoundException as e:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.args)
#
#     return Response(status_code=HTTPStatus.NO_CONTENT.value)
