import fastapi
from sqlmodel import Session

from cmrad_user_institution_api.app import institution_service, user_service
from cmrad_user_institution_api.infrastructure import database
from cmrad_user_institution_api.infrastructure.repositories import (
    institution_repository,
    user_repository,
)


def get_user_service(
    session: Session = fastapi.Depends(database.get_db_session),
) -> user_service.UserService:
    user_repo = user_repository.UserRepository(session)
    return user_service.UserService(user_repo)


def get_institution_service(
    session: Session = fastapi.Depends(database.get_db_session),
) -> institution_service.InstitutionService:
    institution_repo = institution_repository.InstitutionRepository(session)
    return institution_service.InstitutionService(institution_repo)
