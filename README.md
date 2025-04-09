# user-institution-api

## Summary

This is a simple API that facilitates the management of users and institutions along with relations between the two entities. The API is implemented in Python using FastAPI and uses SQLite as the database.

## Key Constraints

* Users have the following attributes:
  * First Name
  * Last Name
  * Email
* Institutions have the following attributes:
  * Institution Name
  * User count
* Users can belong to multiple institutions
  * Users can belong to only one primary institution

## Setup

* Clone the repository
* Run `make run` command to build the docker image and run the application
  * The application will be available at `http://0.0.0.0:8000` by default
  * There is no authentication required for this simple API
* Run `make test` to run the unit tests
* Run `make format` to format the code using flake8, isort and black
* Run `make simulate` to run the following simulation:
  * Create user entity
  * Get user entity
  * Create institution entity
  * Get institution entity
  * Create primary user-institution relation
  * Get institution entity (to see user count)
  * Create second institution
  * Create non-primary user-institution relation (demonstrates multiple institution relations)
  * Create third institution
  * Create second primary user-institution relation (will fail as user already has a primary institution)

## API Endpoints

* POST `users/`
* GET `users/`
* GET `users/{user_id}`
* PUT `users/{user_id}`
* DELETE `users/{user_id}`
* POST `institutions/`
* GET `institutions/`
* GET `institutions/{institution_id}`
* PUT `institutions/{institution_id}`
* DELETE `institutions/{institution_id}`
* POST `users/{user_id}/institutions/{institution_id}`
* GET `users/{user_id}/institutions/{institution_id}`

See `src/user_institution_api/api/models.py` for request and response models. 

## Important Design Decisions
* Implemented following a Domain Driven Design (DDD) approach
  * Implemented three distinct models relating to the application level
    * E.g. CreateUserRequest (DTO), User (Entity), UserORM (DAO)
    * Though only a simple application, this emphasises the separation of concerns and makes the code more maintainable.
* Use SQLite for the database
  * The serverless nature of SQLite makes it a good choice for this simple project.
* Use SQLModel for the ORM over pure SQL or SQLAlchemy
  * The advantage of this is the type hinting and the ability to use Pydantic models directly as ORM models.