from domain.models.user.user import User


def exists(user: User) -> bool:
    return not (user is None or user.delete_flag)
