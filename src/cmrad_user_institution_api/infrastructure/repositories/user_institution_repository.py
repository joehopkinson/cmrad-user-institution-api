from typing import Any, Optional

from sqlmodel import Session, select

from cmrad_user_institution_api.domain import user_institution_association
from cmrad_user_institution_api.infrastructure import models
from cmrad_user_institution_api.infrastructure.repositories import abstract_repository


class UserInstitutionRepository(abstract_repository.Repository):
    def __init__(self, session: Session):
        super().__init__()
        self._session = session

    def get_by_user(
        self, user_id: str
    ) -> list[user_institution_association.UserInstitutionAssociation]:
        if not user_id:
            raise ValueError("user_id must be provided")

        statement = select(models.UserInstitutionORM).where(
            models.UserInstitutionORM.user_id == user_id
        )
        return [
            user_institution_association.UserInstitutionAssociation(
                **association_orm.model_dump()
            )
            for association_orm in self._session.exec(statement).all()
        ]

    def get_by_institution(
        self, institution_id: str
    ) -> list[user_institution_association.UserInstitutionAssociation]:
        if not institution_id:
            raise ValueError("institution_id must be provided")

        statement = select(models.UserInstitutionORM).where(
            models.UserInstitutionORM.institution_id == institution_id
        )

        return [
            user_institution_association.UserInstitutionAssociation(
                **association_orm.model_dump()
            )
            for association_orm in self._session.exec(statement).all()
        ]

    def get(
        self, user_id: str, institution_id: str
    ) -> Optional[user_institution_association.UserInstitutionAssociation]:
        statement = select(models.UserInstitutionORM).where(
            models.UserInstitutionORM.user_id == user_id,
            models.UserInstitutionORM.institution_id == institution_id,
        )
        if association_orm := self._session.exec(statement).first():
            return user_institution_association.UserInstitutionAssociation(
                **association_orm.model_dump()
            )
        return None

    def add(
        self, association: user_institution_association.UserInstitutionAssociation
    ) -> None:
        association_orm = models.UserInstitutionORM(**association.as_dict())
        self._session.add(association_orm)
        self._session.commit()
        self._session.refresh(association_orm)

    def update(
        self,
    ) -> user_institution_association.UserInstitutionAssociation:
        raise NotImplementedError

    def get_all(self) -> list[Any]:
        raise NotImplementedError

    def delete(
        self, association: user_institution_association.UserInstitutionAssociation
    ):
        raise NotImplementedError
