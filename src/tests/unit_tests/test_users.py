import json

import pytest

from src.api.models import User

# POST User route


def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"username": "hajar", "email": "hajar@gmail.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "hajar@gmail.com was added!" in data["message"]


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/users",
        data=json.dumps({"email": "sara@gmail.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/users",
        data=json.dumps({"username": "hajar", "email": "hajar@gmail.com"}),
        content_type="application/json",
    )
    resp = client.post(
        "/users",
        data=json.dumps({"username": "hajar", "email": "hajar@gmail.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "This email already exists." in data["message"]

    # Get single user Route


def test_single_user(test_app, test_database, add_user):
    user = add_user("hajar", "hajar@gmail.com")
    client = test_app.test_client()
    resp = client.get(f"/users/{user.id}")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "hajar" in data["username"]
    assert "hajar@gmail.com" in data["email"]


def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


# Get many users Route


def test_all_users(test_app, test_database, add_user):
    # clear table at the start of the test. Reason: the previous test add rows to the tables
    # and assertion for this test fails (2 vs 4 entries in db)
    test_database.session.query(User).delete()
    add_user("sara", "sara@gmail.com")
    add_user("selma", "selma@gmail.com")
    client = test_app.test_client()
    resp = client.get("/users")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert len(data) == 2
    assert "sara" in data[0]["username"]
    assert "sara@gmail.com" in data[0]["email"]
    assert "selma" in data[1]["username"]
    assert "selma@gmail.com" in data[1]["email"]


# Delete a user


def test_remove_user(test_app, test_database, add_user):
    # clear table
    test_database.session.query(User).delete()
    # add to be removed user
    user = add_user("hajar", "hajar@gmail.com")
    client = test_app.test_client()
    resp_one = client.get("/users")
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert len(data) == 1

    resp_two = client.delete(f"/users/{user.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "hajar@gmail.com was removed." in data["message"]

    resp_three = client.get("/users")
    data = json.loads(resp_three.data.decode())
    assert resp_three.status_code == 200
    assert len(data) == 0


def test_remove_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()
    resp = client.delete("/users/999")
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User 999 does not exist" in data["message"]


def test_update_user_duplicate_email(test_app, test_database, add_user):
    user = add_user("zineb", "zineb@gmail.com")

    client = test_app.test_client()
    resp = client.put(
        f"/users/{user.id}",
        data=json.dumps({"username": "zineb", "email": "zineb@gmail.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "This email already exists." in data["message"]


def test_update_user(test_app, test_database, add_user):
    user = add_user("hajar", "hajar@gmail.com")
    client = test_app.test_client()
    resp_one = client.put(
        f"users/{user.id}",
        data=json.dumps({"username": "sara", "email": "sara@gmail.com"}),
        content_type="application/json",
    )
    data = json.loads(resp_one.data.decode())
    assert resp_one.status_code == 200
    assert f"{user.id} was updated!" in data["message"]

    resp_two = client.get(f"/users/{user.id}")
    data = json.loads(resp_two.data.decode())
    assert resp_two.status_code == 200
    assert "sara" in data["username"]
    assert "sara@gmail.com" in data["email"]


@pytest.mark.parametrize(
    "user_id, payload, status_code, message",
    [
        [1, {}, 400, "Input payload validation failed"],
        [1, {"email": "hajar@gmail.com"}, 400, "Input payload validation failed"],
        [
            999,
            {"username": "hajar", "email": "hajar@gmail.com"},
            404,
            "User 999 does not exist",
        ],
    ],
)
def test_update_user_invalid(
    test_app, test_database, user_id, payload, status_code, message
):
    client = test_app.test_client()
    resp = client.put(
        f"/users/{user_id}",
        data=json.dumps(payload),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == status_code
    assert message in data["message"]
