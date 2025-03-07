from typing import Optional

import fastapi

from cmrad_user_institution_api.api import dependencies, models
from cmrad_user_institution_api.app import exceptions
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
    return models.CreateUserResponse(
        message="User created successfully", user_id=user_id
    )


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
) -> Optional[models.GetUserResponse]:
    try:
        user_entity = user_service.get_user(user_id)
        return user_entity
    except exceptions.UserNotFoundError:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))


@app.patch(
    "/users/{user_id}",
    status_code=201,
    response_model=models.GetUserResponse,
)
def update_user(
    user_id: str,
    request: models.UpdateUserRequest,
    user_service: user.UserService = fastapi.Depends(dependencies.get_user_service),
) -> Optional[models.GetUserResponse]:
    try:
        user_entity = user_service.update_user(user_id, request)
        return user_entity
    except exceptions.UserNotFoundError:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    except exceptions.UserUpdateError:
        raise fastapi.HTTPException(status_code=400, detail="Invalid update request")
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))


@app.delete(
    "/users/{user_id}",
    status_code=204,
)
def delete_user(
    user_id: str,
    user_service: user.UserService = fastapi.Depends(dependencies.get_user_service),
) -> None:
    try:
        user_service.delete_user(user_id)
    except exceptions.UserNotFoundError:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))


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
) -> models.CreateInstitutionResponse:
    institution_id = institution_service.create_new_institution(request)
    return models.CreateInstitutionResponse(
        message="Institution created successfully", institution_id=institution_id
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
) -> Optional[models.GetInstitutionResponse]:
    try:
        institution_entity = institution_service.get_institution(institution_id)
        return institution_entity
    except exceptions.InstitutionNotFoundError:
        raise fastapi.HTTPException(status_code=404, detail="Institution not found")
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))


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
) -> Optional[models.GetInstitutionResponse]:
    try:
        institution_entity = institution_service.update_institution(
            institution_id, request
        )
        return institution_entity
    except exceptions.InstitutionNotFoundError:
        raise fastapi.HTTPException(status_code=404, detail="Institution not found")
    except exceptions.InstitutionUpdateError:
        raise fastapi.HTTPException(status_code=400, detail="Invalid update request")
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))


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
    try:
        institution_service.delete_institution(institution_id)
    except exceptions.InstitutionNotFoundError:
        raise fastapi.HTTPException(status_code=404, detail="Institution not found")
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))


@app.post(
    "/users/{user_id}/institutions/{institution_id}",
    status_code=201,
)
def add_user_institution_association(
    user_id: str,
    institution_id: str,
    request: models.AddUserInstitutionAssociationRequest,
    user_service: user.UserService = fastapi.Depends(dependencies.get_user_service),
) -> models.AddUserInstitutionAssociationResponse:
    try:
        user_service.add_user_institution_association(user_id, institution_id, request)
    except exceptions.UserNotFoundError:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    except exceptions.InstitutionNotFoundError:
        raise fastapi.HTTPException(status_code=404, detail="Institution not found")
    except exceptions.ExistingUserInstitutionAssociationError:
        raise fastapi.HTTPException(
            status_code=409, detail="User-institution association already exists"
        )
    except exceptions.InvalidUserInstitutionAssociationError:
        raise fastapi.HTTPException(
            status_code=400, detail="Invalid user-institution association"
        )
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))
    return models.AddUserInstitutionAssociationResponse(
        message="Association created successfully",
        user_id=user_id,
        institution_id=institution_id,
    )


@app.get(
    "/users/{user_id}/institutions",
    status_code=200,
    response_model=models.GetUserInstitutionAssociationResponse,
)
def get_user_institution_associations(
    user_id: str,
    user_service: user.UserService = fastapi.Depends(dependencies.get_user_service),
) -> models.GetUserInstitutionAssociationResponse:
    try:
        return user_service.get_user_institution_associations(user_id)
    except exceptions.UserNotFoundError:
        raise fastapi.HTTPException(status_code=404, detail="User not found")
    except exceptions.InstitutionNotFoundError:
        raise fastapi.HTTPException(status_code=404, detail="Institution not found")
    except Exception as e:
        raise fastapi.HTTPException(status_code=500, detail=str(e))
