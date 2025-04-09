import pydantic


class EmailAddress(pydantic.BaseModel):
    value: str

    @pydantic.field_validator("value")
    def validate_email_address(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email format")
        return v
