import fastapi

from cmrad_user_institution_api.api import dependencies, models
from cmrad_user_institution_api.app import institution_service as institution
from cmrad_user_institution_api.app import user_service as user

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
    user_service: user.UserService = fastapi.Depends(dependencies.get_user_service),
) -> models.CreateUserResponse:
    user_id = user_service.create_new_user(request)
    return models.CreateUserResponse(message=f"User created with id: {user_id}")


@app.get(
    "/users",
    status_code=200,
    response_model=list[models.GetUserResponse],
)
def get_users(
    user_service: user.UserService = fastapi.Depends(dependencies.get_user_service),
) -> list[models.GetUserResponse]:
    return user_service.get_users()


@app.get(
    "/users/{user_id}",
    status_code=200,
    response_model=models.GetUserResponse,
)
def get_user(
    user_id: str,
    user_service: user.UserService = fastapi.Depends(dependencies.get_user_service),
) -> models.GetUserResponse:
    user_entity = user_service.get_user(user_id)
    if not user_entity:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return user_entity


@app.patch(
    "/users/{user_id}",
    status_code=201,
    response_model=models.GetUserResponse,
)
def update_user(
    user_id: str,
    request: models.UpdateUserRequest,
    user_service: user.UserService = fastapi.Depends(dependencies.get_user_service),
) -> models.GetUserResponse:
    user_entity = user_service.update_user(user_id, request)
    if not user_entity:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    return user_entity


@app.delete(
    "/users/{user_id}",
    status_code=204,
)
def delete_user(
    user_id: str,
    user_service: user.UserService = fastapi.Depends(dependencies.get_user_service),
) -> None:
    if not user_service.delete_user(user_id):
        raise fastapi.HTTPException(status_code=404, detail="User not found")


@app.post(
    "/institutions",
    status_code=201,
    response_model=models.CreateInstitutionResponse,
)
def create_institution(
    request: models.CreateInstitutionRequest,
    institution_service: institution.InstitutionService = fastapi.Depends(
        dependencies.get_institution_service
    ),
) -> models.CreateUserResponse:
    institution_id = institution_service.create_new_institution(request)
    return models.CreateUserResponse(
        message=f"Institution created with id: {institution_id}"
    )


@app.get(
    "/institutions",
    status_code=200,
    response_model=list[models.GetInstitutionResponse],
)
def get_institutions(
    institution_service: institution.InstitutionService = fastapi.Depends(
        dependencies.get_institution_service
    ),
) -> list[models.GetInstitutionResponse]:
    return institution_service.get_institutions()


@app.get(
    "/institutions/{institution_id}",
    status_code=200,
    response_model=models.GetInstitutionResponse,
)
def get_institution(
    institution_id: str,
    institution_service: institution.InstitutionService = fastapi.Depends(
        dependencies.get_institution_service
    ),
) -> models.GetInstitutionResponse:
    institution_entity = institution_service.get_institution(institution_id)
    if not institution_entity:
        raise fastapi.HTTPException(status_code=404, detail="Institution not found")
    return institution_entity


@app.patch(
    "/institutions/{institution_id}",
    status_code=201,
    response_model=models.GetInstitutionResponse,
)
def update_institution(
    institution_id: str,
    request: models.UpdateInstitutionRequest,
    institution_service: institution.InstitutionService = fastapi.Depends(
        dependencies.get_institution_service
    ),
) -> models.GetInstitutionResponse:
    institution_entity = institution_service.update_institution(institution_id, request)
    if not institution_entity:
        raise fastapi.HTTPException(status_code=404, detail="Institution not found")
    return institution_entity


@app.delete(
    "/institutions/{institution_id}",
    status_code=204,
)
def delete_institution(
    institution_id: str,
    institution_service: institution.InstitutionService = fastapi.Depends(
        dependencies.get_institution_service
    ),
) -> None:
    if not institution_service.delete_institution(institution_id):
        raise fastapi.HTTPException(status_code=404, detail="Institution not found")
