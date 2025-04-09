from typing import Optional

from user_institution_api.api import models
from user_institution_api.app import exceptions
from user_institution_api.domain import user as user_entity
from user_institution_api.domain import (
    user_institution_association as user_institution_association_entity,
)
from user_institution_api.infrastructure.repositories import (
    institution_repository,
    user_institution_repository,
    user_repository,
)


class UserService:
    def __init__(
        self,
        user_repo: user_repository.UserRepository,
        institution_repo: institution_repository.InstitutionRepository,
        user_institution_repo: user_institution_repository.UserInstitutionRepository,
    ):
        self._user_repo = user_repo
        self._institution_repo = institution_repo
        self._user_institution_repo = user_institution_repo

    def create_new_user(self, request: models.CreateUserRequest) -> str:
        user = user_entity.UserFactory.create_user(**request.model_dump())
        self._user_repo.add(user)
        return user.user_id

    def get_users(self) -> list[models.GetUserResponse]:
        users = self._user_repo.get_all()
        return [models.GetUserResponse(**user.as_dict()) for user in users]

    def get_user(self, user_id: str) -> Optional[models.GetUserResponse]:
        if user := self._user_repo.get(user_id):
            return models.GetUserResponse(**user.as_dict())
        raise exceptions.UserNotFoundError

    def update_user(
        self, user_id: str, request: models.UpdateUserRequest
    ) -> Optional[models.GetUserResponse]:
        if user := self._user_repo.get(user_id):
            try:
                properties = user_entity.UserFactory.validate_properties(
                    **request.model_dump()
                )
                updated_user = self._user_repo.update(user.user_id, properties)
                return models.GetUserResponse(**updated_user.as_dict())
            except Exception:
                raise exceptions.UserUpdateError
        raise exceptions.UserNotFoundError

    def delete_user(self, user_id: str) -> None:
        if user := self._user_repo.get(user_id):
            self._user_repo.delete(user)
        raise exceptions.UserNotFoundError

    def get_user_institution_associations(
        self, user_id: str
    ) -> models.GetUserInstitutionAssociationResponse:
        if user := self._user_repo.get(user_id):
            associations = self._user_institution_repo.get_by_user(user.user_id)
            institution_ids = []
            primary_institution_id = None
            for association in associations:
                if association.is_primary:
                    primary_institution_id = association.institution_id
                institution_ids.append(association.institution_id)
            return models.GetUserInstitutionAssociationResponse(
                user_id=user.user_id,
                institution_ids=institution_ids,
                primary_institution_id=primary_institution_id,
            )
        raise ValueError(f"User with id {user_id} not found")

    def add_user_institution_association(
        self,
        user_id: str,
        institution_id: str,
        request: models.AddUserInstitutionAssociationRequest,
    ) -> None:
        # Validate that the user and institution exist
        user = self._user_repo.get(user_id)
        if not user:
            raise exceptions.UserNotFoundError

        institution = self._institution_repo.get(institution_id)
        if not institution:
            raise exceptions.InstitutionNotFoundError

        if self._user_institution_repo.get(user.user_id, institution.institution_id):
            raise exceptions.ExistingUserInstitutionAssociationError

        proposed_association = user_institution_association_entity.UserInstitutionAssociationFactory.create_association(
            user_id=user.user_id,
            institution_id=institution.institution_id,
            is_primary=request.is_primary,
        )

        # Validate that the association is valid
        existing_associations = self._user_institution_repo.get_by_user(user.user_id)
        try:
            user.validate_institution_association(
                proposed_association, existing_associations
            )
        except Exception:
            raise exceptions.InvalidUserInstitutionAssociationError

        self._user_institution_repo.add(proposed_association)
