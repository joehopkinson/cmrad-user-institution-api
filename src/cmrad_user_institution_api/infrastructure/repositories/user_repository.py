from typing import Optional

from sqlmodel import Session, select

from cmrad_user_institution_api.domain import user as user_entity
from cmrad_user_institution_api.infrastructure import models
from cmrad_user_institution_api.infrastructure.repositories import abstract_repository


class UserRepository(abstract_repository.Repository):
    def __init__(self, session: Session):
        super().__init__()
        self._session = session

    def get(self, user_id: str) -> Optional[user_entity.User]:
        if user_orm := self._session.get(models.UserORM, user_id):
            return user_entity.User(**user_orm.model_dump())
        return None

    def get_all(self) -> list[user_entity.User]:
        user_orms = self._session.exec(select(models.UserORM)).all()
        return [user_entity.User(**user_orm.model_dump()) for user_orm in user_orms]

    def add(self, user: user_entity.User) -> None:
        user_orm = models.UserORM(**user.as_dict())
        self._session.add(user_orm)
        self._session.commit()
        self._session.refresh(user_orm)

    def update(
        self, user_id: str, updated_fields: dict[str, str]
    ) -> Optional[user_entity.User]:
        if user_orm := self._session.get(models.UserORM, user_id):
            for key, value in updated_fields.items():
                if hasattr(user_orm, key) and value is not None:
                    setattr(user_orm, key, value)
            self._session.commit()
            self._session.refresh(user_orm)
            return user_entity.User(**user_orm.model_dump())
        return None

    def delete(self, user: user_entity.User) -> None:
        user_orm = self._session.get(models.UserORM, user.user_id)
        self._session.delete(user_orm)
        self._session.commit()
