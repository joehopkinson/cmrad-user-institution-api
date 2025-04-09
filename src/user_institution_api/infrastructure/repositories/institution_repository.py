from typing import Optional

from sqlmodel import Session, func, select

from user_institution_api.domain import institution as institution_entity
from user_institution_api.infrastructure import models
from user_institution_api.infrastructure.repositories import abstract_repository


class InstitutionRepository(abstract_repository.Repository):
    def __init__(self, session: Session):
        super().__init__()
        self._session = session

    @staticmethod
    def _user_count_query(institution_id: Optional[str] = None) -> select:
        query = (
            select(
                models.InstitutionORM,
                func.count(models.UserInstitutionORM.user_id).label("user_count"),
            )
            .join(
                models.UserInstitutionORM,
                models.UserInstitutionORM.institution_id  # type: ignore
                == models.InstitutionORM.institution_id,
                isouter=True,
            )
            .group_by(models.InstitutionORM.institution_id)
        )
        if institution_id:
            query = query.where(models.InstitutionORM.institution_id == institution_id)
        return query

    def get(self, institution_id: str) -> Optional[institution_entity.Institution]:
        if result := self._session.exec(self._user_count_query(institution_id)).first():
            institution_orm, user_count = result
            return institution_entity.Institution(
                **institution_orm.model_dump(), user_count=user_count
            )
        return None

    def get_all(self) -> list[institution_entity.Institution]:
        return [
            institution_entity.Institution(
                **institution_orm.model_dump(), user_count=user_count
            )
            for institution_orm, user_count in self._session.exec(
                self._user_count_query()
            ).all()
        ]

    def add(self, institution: institution_entity.Institution) -> None:
        institution_orm = models.InstitutionORM(**institution.as_dict())
        self._session.add(institution_orm)
        self._session.commit()
        self._session.refresh(institution_orm)

    def update(
        self, institution_id: str, updated_fields: dict[str, str]
    ) -> Optional[institution_entity.Institution]:
        if institution_orm := self._session.get(models.InstitutionORM, institution_id):
            for key, value in updated_fields.items():
                if hasattr(institution_orm, key) and value is not None:
                    setattr(institution_orm, key, value)
            self._session.commit()
            self._session.refresh(institution_orm)
            return institution_entity.Institution(**institution_orm.model_dump())
        return None

    def delete(self, institution: institution_entity.Institution) -> None:
        institution_orm = self._session.get(
            models.InstitutionORM, institution.institution_id
        )
        self._session.delete(institution_orm)
        self._session.commit()
