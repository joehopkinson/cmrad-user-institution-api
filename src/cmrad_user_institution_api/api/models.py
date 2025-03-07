from typing import Optional

import pydantic


class BaseRequest(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")


class CreateUserRequest(BaseRequest):
    email_address: str
    first_name: str
    last_name: str


class UpdateUserRequest(BaseRequest):
    email_address: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class CreateUserResponse(pydantic.BaseModel):
    message: str
    user_id: str


class GetUserResponse(pydantic.BaseModel):
    user_id: str
    email_address: str
    first_name: str
    last_name: str


class CreateInstitutionRequest(BaseRequest):
    institution_name: str


class UpdateInstitutionRequest(BaseRequest):
    institution_name: Optional[str] = None


class CreateInstitutionResponse(pydantic.BaseModel):
    message: str
    institution_id: str


class GetInstitutionResponse(pydantic.BaseModel):
    institution_id: str
    institution_name: str
    user_count: int


class AddUserInstitutionAssociationRequest(BaseRequest):
    is_primary: Optional[bool] = False


class AddUserInstitutionAssociationResponse(pydantic.BaseModel):
    message: str
    user_id: str
    institution_id: str


class GetUserInstitutionAssociationResponse(pydantic.BaseModel):
    user_id: str
    primary_institution_id: Optional[str] = None
    institution_ids: list[str] = None


class AssignPrimaryUserInstitutionAssociationResponse(pydantic.BaseModel):
    message: str
    user_id: str
    institution_id: str
