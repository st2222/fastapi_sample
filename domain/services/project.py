from domain.models.project.project import Project


def exists(project: Project) -> bool:
    return not (project is None)
