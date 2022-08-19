from datetime import datetime
from http import HTTPStatus

from starlette.responses import Response

from pydantic import BaseModel
from typing import Dict, Optional, List
from application.report import register, select_all_reports, find_report, update_report
from domain.models.date import Date
from domain.models.project.project_id import ProjectId
from domain.models.report.comment import Comment
from domain.models.report.plan import Plan
from domain.models.report.report import Report
from fastapi import APIRouter, HTTPException, Depends

from domain.models.report.report_id import ReportId
from domain.models.report_detail.hour import Hour
from domain.models.report_detail.report_detail import ReportDetail
from domain.models.report_detail.report_detail_id import ReportDetailId
from domain.models.user.user_id import UserId
from exception.exception import NotFoundException
from routers.auth import oauth2_scheme

router = APIRouter()


class ReportDetailModel(BaseModel):
    report_detail_id: Optional[int] = None
    user_id: Optional[int] = None
    project_id: Optional[int] = None
    hour: Optional[int] = None


class ReportModel(BaseModel):
    report_id: Optional[int] = None
    user_id: Optional[int] = None
    date: Optional[datetime] = None
    comment: Optional[str] = None
    plan: Optional[str] = None
    report_detail: List[ReportDetailModel] = []

    def to_report(self) -> Report:
        return Report(report_id=ReportId(self.report_id), user_id=UserId(self.user_id),
                      date=self.date, comment=Comment(self.comment), plan=Plan(self.plan),
                      report_detail=list(
                          map(lambda x: ReportDetail(report_detail_id=ReportDetailId(x.report_detail_id),
                                                     report_id=ReportId(self.report_id),
                                                     project_id=ProjectId(x.project_id), hour=Hour(x.hour)),
                              self.report_detail)))


@router.post('/reports')
def create_report(report_model: ReportModel, token=Depends(oauth2_scheme)) -> Response:
    register(report_model.to_report())
    # return {"message": 'ok'}
    return Response(status_code=HTTPStatus.OK.value)


@router.get('/reports')
def get_reports(token=Depends(oauth2_scheme)) -> List:
    return list(
        map(lambda x: ReportModel(report_id=x.report_id.value, user_id=x.user_id.value,
                                  date=x.date, comment=x.comment.value, plan=x.plan.value,
                                  report_detail=list(
                                      map(lambda y: ReportDetailModel(report_detail_id=y.report_detail_id.value,
                                                                      report_id=y.report_id.value,
                                                                      project_id=y.project_id.value,
                                                                      hour=y.hour.value), x.report_detail))),
            select_all_reports()))


@router.get('/reports/{report_id}')
def get_report_by_id(report_id: int, token=Depends(oauth2_scheme)) -> ReportModel:
    try:
        report: Report = find_report(ReportId(report_id))
    except NotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.args)

    return ReportModel(report_id=report.report_id.value, user_id=report.user_id.value,
                       date=report.date, comment=report.comment.value, plan=report.plan.value,
                       report_detail=list(
                           map(lambda y: ReportDetailModel(report_detail_id=y.report_detail_id.value,
                                                           report_id=y.report_id.value,
                                                           project_id=y.project_id.value,
                                                           hour=y.hour.value), report.report_detail)))


@router.patch('/reports/{report_id}')
def update_report_by_id(report_id: int, report_model: ReportModel, token=Depends(oauth2_scheme)) -> Response:
    try:
        update_report(ReportId(report_id), report_model.dict(exclude_unset=True))
    except NotFoundException as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.args)

    return Response(status_code=HTTPStatus.OK.value)

# @router.delete('/reports/{report_id}', status_code=HTTPStatus.NO_CONTENT)
# def delete_report_by_id(report_id: int) -> Response:
#     try:
#         delete_report(ReportId(report_id))
#     except NotFoundException as e:
#         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=e.args)
#
#     return Response(status_code=HTTPStatus.NO_CONTENT.value)
