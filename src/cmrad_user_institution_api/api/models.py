from typing import Optional

import pydantic


class BaseRequest(pydantic.BaseModel):
    class Config:
        extra = "forbid"


class CreateUserRequest(BaseRequest):
    email_address: str
    first_name: str
    last_name: str
    institution_id: Optional[str] = None


class UpdateUserRequest(BaseRequest):
    email_address: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    institution_id: Optional[str] = None


class CreateUserResponse(pydantic.BaseModel):
    message: str


class GetUserResponse(pydantic.BaseModel):
    user_id: str
    email_address: str
    first_name: str
    last_name: str
    institution_id: Optional[str] = None


class CreateInstitutionRequest(BaseRequest):
    institution_name: str


class UpdateInstitutionRequest(BaseRequest):
    institution_name: Optional[str] = None


class CreateInstitutionResponse(pydantic.BaseModel):
    message: str


class GetInstitutionResponse(pydantic.BaseModel):
    institution_id: str
    institution_name: str
