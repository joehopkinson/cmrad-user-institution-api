from cmrad_user_institution_api.api import models
from cmrad_user_institution_api.domain import user_entity


class UserService:
    def __init__(self):
        pass

    def create_new_user(self, request: models.CreateUserRequest) -> str:
        user = user_entity.create_user(
            first_name=request.first_name,
            last_name=request.last_name,
            email_address=request.email_address,
        )
        return user.user_id
