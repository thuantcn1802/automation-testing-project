import pytest

pytestmark = pytest.mark.api


def test_registration_with_empty_body_returns_required_field_errors(api):
    """Goal: check server-side validation of required registration fields.
    Precondition: the request body is an empty JSON object.
    Expected: HTTP 422 with validation errors for email and password."""
    response = api.post("/users/register", data={})

    assert response.status == 422, response.text()
    errors = response.json()
    assert errors.get("email"), errors
    assert errors.get("password"), errors


def test_user_profile_with_bearer_auth_returns_own_email(api, request, test_user):
    """Goal: fetch the authenticated user's profile.
    Precondition: the auth fixture signed in with a dedicated test account.
    Expected: HTTP 200 and the email of that test account."""
    # Keep the authorization header out of pytest's test argument display.
    response = api.get("/users/me", headers=request.getfixturevalue("auth_headers"))

    assert response.status == 200
    assert response.json()["email"] == test_user["email"]
