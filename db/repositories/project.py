from abc import ABC, abstractmethod
from typing import Optional, Dict
from sqlalchemy import func, false
from db.models.report_detail import ReportDetailDataModel
from db.models.user import UserDataModel
from domain.models.chart.project_with_total_time import ProjectWithTotalTime
from domain.models.project.budget import Budget
from domain.models.project.other_cost import OtherCost
from domain.models.project.profit_rate import ProfitRate
from domain.models.project.project_id import ProjectId
from typing import List
from db.setting.setting import session, ENGINE
from db.models.project import ProjectDataModel
from domain.models.project.project import Project
from domain.models.project.project_name import ProjectName
from domain.models.project.status import Status
from domain.models.report_detail.hour import Hour


class ProjectRepository(ABC):

    @abstractmethod
    def insert(self, project: Project) -> None:
        pass

    @abstractmethod
    def select(self) -> List[Project]:
        pass

    @abstractmethod
    def find_project(self, project: Project) -> Optional[Project]:
        pass

    @abstractmethod
    def update_project(self, project_id: ProjectId, body: Dict) -> None:
        pass

    @abstractmethod
    def delete_project(self, project: Project) -> None:
        pass

    @abstractmethod
    def select_projects_with_total_time(self):
        pass


class ProjectRepositoryImpl(ProjectRepository):

    def insert(self, project: Project) -> None:
        project_data_model: ProjectDataModel = to_project_data_model(project)

        try:
            session.add(project_data_model)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        session.close()

    def select(self) -> List[Project]:
        return list(map(lambda x: to_project(x),
                        session.query(ProjectDataModel).all()))

    def find_project(self, project_id: ProjectId) -> Optional[Project]:
        project_data_model = session.query(ProjectDataModel).filter(
            ProjectDataModel.project_id == project_id.value).first()
        if project_data_model is None:
            return None
        return to_project(project_data_model)

    def update_project(self, project_id: ProjectId, body: Dict) -> None:
        try:
            project_data_model: ProjectDataModel = session.query(ProjectDataModel).filter(
                ProjectDataModel.project_id == project_id.value).first()
            for key, value in body.items():
                print(setattr(project_data_model, key, value))
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        session.close()

    def delete_project(self, project: Project) -> None:
        try:
            project_data_model: ProjectDataModel = session.query(ProjectDataModel).filter(
                ProjectDataModel.project_id == project.project_id.value).first()
            project_data_model.delete_flag = True
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        session.close()

    def select_projects_with_total_time(self) -> List[ProjectWithTotalTime]:
        projects_data_model_with_total_time: List = session.query(
            ProjectDataModel.project_id,
            ProjectDataModel.project_name,
            ProjectDataModel.budget,
            ProjectDataModel.other_cost,
            ProjectDataModel.profit_rate,
            ProjectDataModel.status,
            func.sum(ReportDetailDataModel.hour).label("total_time")) \
            .join(ReportDetailDataModel).group_by(ProjectDataModel.project_id).all()

        projects_with_total_time: List[ProjectWithTotalTime] = list(
            map(lambda x: ProjectWithTotalTime(project_id=ProjectId(x['project_id']),
                                               project_name=ProjectName(x['project_name']),
                                               budget=Budget(x['budget']), other_cost=OtherCost(x['other_cost']),
                                               profit_rate=ProfitRate(x['profit_rate']), status=Status(x['status']),
                                               total_time=Hour(x['total_time'])),
                projects_data_model_with_total_time))

        return projects_with_total_time


def to_project_data_model(project: Project) -> ProjectDataModel:
    project_data_model = ProjectDataModel()
    # project_data_model.project_id = project.project_id
    project_data_model.project_name = project.project_name.value
    project_data_model.budget = project.budget.value
    project_data_model.status = project.status.value
    project_data_model.other_cost = project.other_cost.value
    project_data_model.profit_rate = project.profit_rate.value

    return project_data_model


def to_project(project_data_model: ProjectDataModel) -> Project:
    project = Project(project_id=ProjectId(project_data_model.project_id),
                      project_name=ProjectName(project_data_model.project_name),
                      budget=Budget(project_data_model.budget),
                      status=Status(project_data_model.status),
                      other_cost=OtherCost(project_data_model.other_cost),
                      profit_rate=ProfitRate(project_data_model.profit_rate))

    return project
