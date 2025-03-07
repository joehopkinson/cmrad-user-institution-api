from typing import Optional

from cmrad_user_institution_api.api import models
from cmrad_user_institution_api.app import exceptions
from cmrad_user_institution_api.domain import institution as institution_entity
from cmrad_user_institution_api.infrastructure.repositories import (
    institution_repository,
)


class InstitutionService:
    def __init__(
        self,
        institution_repo: institution_repository.InstitutionRepository,
    ):
        self._institution_repo = institution_repo

    def create_new_institution(self, request: models.CreateInstitutionRequest) -> str:
        institution = institution_entity.InstitutionFactory.create_institution(
            institution_name=request.institution_name
        )
        self._institution_repo.add(institution)
        return institution.institution_id

    def get_institutions(self) -> list[models.GetInstitutionResponse]:
        institutions = self._institution_repo.get_all()
        return [
            models.GetInstitutionResponse(**institution.as_dict())
            for institution in institutions
        ]

    def get_institution(
        self, institution_id: str
    ) -> Optional[models.GetInstitutionResponse]:
        if institution := self._institution_repo.get(institution_id):
            return models.GetInstitutionResponse(**institution.as_dict())
        return None

    def update_institution(
        self, institution_id: str, request: models.UpdateInstitutionRequest
    ) -> Optional[models.GetInstitutionResponse]:
        if institution := self._institution_repo.get(institution_id):
            try:
                properties = institution_entity.InstitutionFactory.validate_properties(
                    **request.model_dump()
                )
                updated_institution = self._institution_repo.update(
                    institution.institution_id, properties
                )
                return models.GetInstitutionResponse(**updated_institution.as_dict())
            except Exception:
                raise exceptions.InstitutionUpdateError
        raise exceptions.InstitutionNotFoundError

    def delete_institution(self, institution_id: str) -> bool:
        if institution := self._institution_repo.get(institution_id):
            self._institution_repo.delete(institution)
            return True
        return False
