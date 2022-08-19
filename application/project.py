from domain.models.project.project_id import ProjectId
from typing import List
from db.repositories.project import ProjectRepositoryImpl
from domain.models.project.project import Project
from domain.services.project import exists
from exception.exception import NotFoundException

rep = ProjectRepositoryImpl()


def register(project: Project) -> None:
    rep.insert(project)


def select_all_projects() -> List[Project]:
    return rep.select()


def find_project(project_id: ProjectId) -> Project:
    project: Project = rep.find_project(project_id)
    if not exists(project):
        raise NotFoundException(f'{project_id.value} is not found')
    return project


# def delete_project(project_id: ProjectId) -> None:
#     project: Project = rep.find_project(project_id)
#     if not exists(project):
#         raise NotFoundException(f'{project_id.value} is not found')
#     rep.delete_project(project)


def update_project(project_id: ProjectId, body) -> None:
    project: Project = rep.find_project(project_id)
    if not exists(project):
        raise NotFoundException(f'{project_id.value} is not found')
    rep.update_project(project_id, body)
