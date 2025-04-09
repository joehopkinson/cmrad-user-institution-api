from sqlmodel import Field, Relationship, SQLModel


class UserORM(SQLModel, table=True):
    user_id: str = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email_address: str
    institutions: list["UserInstitutionORM"] = Relationship(back_populates="user")


class InstitutionORM(SQLModel, table=True):
    institution_id: str = Field(default=None, primary_key=True)
    institution_name: str
    users: list["UserInstitutionORM"] = Relationship(back_populates="institution")


class UserInstitutionORM(SQLModel, table=True):
    user_id: str = Field(foreign_key="userorm.user_id", primary_key=True)
    institution_id: str = Field(
        foreign_key="institutionorm.institution_id", primary_key=True
    )
    is_primary: bool = Field(default=False)
    user: UserORM = Relationship(back_populates="institutions")
    institution: InstitutionORM = Relationship(back_populates="users")
