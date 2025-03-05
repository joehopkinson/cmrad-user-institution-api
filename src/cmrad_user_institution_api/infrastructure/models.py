from sqlmodel import Field, SQLModel


class UserORM(SQLModel, table=True):
    user_id: str = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email_address: str


class InstitutionORM(SQLModel, table=True):
    institution_id: str = Field(default=None, primary_key=True)
    institution_name: str
