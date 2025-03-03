import pydantic


class CreateUserRequest(pydantic.BaseModel):
    email_address: str
    first_name: str
    last_name: str


class CreateUserResponse(pydantic.BaseModel):
    message: str
