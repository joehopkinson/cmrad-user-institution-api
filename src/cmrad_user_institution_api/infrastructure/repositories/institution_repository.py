from typing import Optional

from sqlmodel import Session, select

from cmrad_user_institution_api.domain import institution_entity
from cmrad_user_institution_api.infrastructure import models
from cmrad_user_institution_api.infrastructure.repositories import abstract_repository


class InstitutionRepository(abstract_repository.Repository):
    def __init__(self, session: Session):
        super().__init__()
        self._session = session

    def get(self, institution_id: str) -> Optional[institution_entity.Institution]:
        if institution_id_orm := self._session.get(
            models.InstitutionORM, institution_id
        ):
            return institution_entity.Institution(**institution_id_orm.model_dump())
        return None

    def get_all(self) -> list[institution_entity.Institution]:
        institution_orms = self._session.exec(select(models.InstitutionORM)).all()
        return [
            institution_entity.Institution(**institution_orm.model_dump())
            for institution_orm in institution_orms
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
