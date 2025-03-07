import time

import requests

ENDPOINT_URL = "http://0.0.0.0:8000"


def create_user():
    user_data = {
        "email_address": "testuser@example.com",
        "first_name": "John",
        "last_name": "Doe",
    }
    response = requests.post(f"{ENDPOINT_URL}/users/", json=user_data)
    return response.json()


def get_user(user_id):
    response = requests.get(f"{ENDPOINT_URL}/users/{user_id}")
    return response.json()


def create_institution(name):
    institution_data = {"institution_name": name}
    response = requests.post(f"{ENDPOINT_URL}/institutions/", json=institution_data)
    return response.json()


def get_institution(institution_id):
    response = requests.get(f"{ENDPOINT_URL}/institutions/{institution_id}")
    return response.json()


def create_user_institution_relation(user_id, institution_id, is_primary=False):
    relation_data = {"is_primary": is_primary}
    response = requests.post(
        f"{ENDPOINT_URL}/users/{user_id}/institutions/{institution_id}",
        json=relation_data,
    )
    return response.json()


def get_user_institution_relation(user_id, institution_id):
    response = requests.get(
        f"{ENDPOINT_URL}/users/{user_id}/institutions/{institution_id}"
    )
    return response.json()


def run_simulation():
    # Create user entity
    user = create_user()
    user_id = user["user_id"]
    print("Created user with user_id:", user_id)
    print()
    time.sleep(1)

    # Get user entity
    user_data = get_user(user_id)
    print("Fetched User:", user_data)
    print()
    time.sleep(1)

    # Create institution entity (first institution)
    institution1 = create_institution("Institution One")
    institution1_institution_id = institution1["institution_id"]
    print(
        "Created first institution with institution_id: ", institution1_institution_id
    )
    print()
    time.sleep(1)

    # Get institution entity to see user count
    institution1_data = get_institution(institution1_institution_id)
    print("Institution 1 Data:", institution1_data)
    print()
    time.sleep(1)

    # Create primary user-institution relation
    response = create_user_institution_relation(
        user_id, institution1_institution_id, is_primary=True
    )
    print(response)
    print()
    time.sleep(1)

    # Get institution entity to see user count
    institution1_data = get_institution(institution1_institution_id)
    print("Institution 1 Data:", institution1_data)
    print()
    time.sleep(1)

    # Create second institution entity
    institution2 = create_institution("Institution Two")
    institution2_institution_id = institution2["institution_id"]
    print(
        "Created second institution with institution_id: ", institution2_institution_id
    )
    print()
    time.sleep(1)

    # Create non-primary user-institution relation (user can belong to multiple institutions)
    response = create_user_institution_relation(
        user_id, institution2_institution_id, is_primary=False
    )
    print(response)
    print()
    time.sleep(1)

    # Create third institution entity
    institution3 = create_institution("Institution Three")
    institution3_institution_id = institution3["institution_id"]
    print(
        "Created third institution with institution_id: ", institution3_institution_id
    )
    print()
    time.sleep(1)

    # Create second primary user-institution relation (will fail if user already has a primary institution)
    print(
        f"Attempting to create a second primary user-institution relation for user {user_id}. (Should fail)"
    )
    response = create_user_institution_relation(
        user_id, institution3_institution_id, is_primary=True
    )
    print(response)


if __name__ == "__main__":
    time.sleep(2)
    run_simulation()
