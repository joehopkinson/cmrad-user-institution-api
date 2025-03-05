from typing import Optional

from cmrad_user_institution_api.api import models
from cmrad_user_institution_api.domain import models as domain_models
from cmrad_user_institution_api.domain import user_entity
from cmrad_user_institution_api.infrastructure.repositories import user_repository


class UserService:
    def __init__(self, user_repo: user_repository.UserRepository):
        self._user_repo = user_repo

    def create_new_user(self, request: models.CreateUserRequest) -> str:
        user = user_entity.UserFactory.create_user(
            first_name=request.first_name,
            last_name=request.last_name,
            email_address=request.email_address,
        )
        self._user_repo.add(user)
        return user.user_id

    def get_users(self) -> list[models.GetUserResponse]:
        users = self._user_repo.get_all()
        return [models.GetUserResponse(**user.as_dict()) for user in users]

    def get_user(self, user_id: str) -> Optional[models.GetUserResponse]:
        if user := self._user_repo.get(user_id):
            return models.GetUserResponse(**user.as_dict())
        return None

    def update_user(
        self, user_id: str, request: models.UpdateUserRequest
    ) -> Optional[models.GetUserResponse]:
        if request.email_address:
            # Instantiating the User entity domain object before updating would require an additional database call
            # To avoid this, perform value object limited validation here
            # If complexity of validation increases, consider moving this to the User entity
            valid_email_address = domain_models.EmailAddress(
                value=request.email_address
            )
            request.email_address = valid_email_address.value

        if user := self._user_repo.update(user_id, request.model_dump()):
            return models.GetUserResponse(**user.as_dict())
        return None

    def delete_user(self, user_id: str) -> bool:
        if user := self._user_repo.get(user_id):
            self._user_repo.delete(user)
            return True
        return False
