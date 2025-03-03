from cmrad_user_institution_api.domain import user_entity
from cmrad_user_institution_api.infrastructure.repositories import abstract_repository


class UserRepository(abstract_repository.Repository):
    """TODO"""

    def __init__(self):
        pass

    def add(self, user: user_entity.User) -> None:
        raise NotImplementedError

    def get(self, id: str) -> user_entity.User:
        raise NotImplementedError
