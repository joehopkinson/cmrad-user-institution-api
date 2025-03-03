import fastapi

from cmrad_user_institution_api.api import models
from cmrad_user_institution_api.app import user_service

app = fastapi.FastAPI(
    title="CMRAD User Institution API",
)


@app.post(
    "/users",
    status_code=201,
    response_model=models.CreateUserResponse,
)
def create_user(
    request: models.CreateUserRequest,
    user_service: user_service.UserService = fastapi.Depends(user_service.UserService),
) -> models.CreateUserResponse:
    user_id = user_service.create_new_user(request)
    return models.CreateUserResponse(message=f"User created with id: {user_id}")
