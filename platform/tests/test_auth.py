import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

PASSWORD = "correct-horse-battery-staple"  # noqa: S105 (test-only)


@pytest.fixture
def owner(db):
    return get_user_model().objects.create_user(username="owner", password=PASSWORD)


def test_anonymous_user_is_redirected_to_login(client):
    response = client.get(reverse("home"))

    assert response.status_code == 302
    assert response.url.startswith(reverse("login"))


def test_login_page_is_public(client):
    assert client.get(reverse("login")).status_code == 200


def test_owner_can_log_in_and_see_dashboard(client, owner):
    response = client.post(
        reverse("login"), {"username": "owner", "password": PASSWORD}, follow=True
    )

    assert response.status_code == 200
    assert response.wsgi_request.user == owner
    assert b"Ready to capture some flags?" in response.content


def test_logout_requires_post_and_logs_out(client, owner):
    client.force_login(owner)

    response = client.post(reverse("logout"))

    assert response.status_code == 302
    assert client.get(reverse("home")).status_code == 302


def test_lockout_after_repeated_failures(client, owner, settings):
    for _ in range(settings.AXES_FAILURE_LIMIT):
        client.post(reverse("login"), {"username": "owner", "password": "wrong"})

    # Even the correct password is refused while locked out.
    response = client.post(reverse("login"), {"username": "owner", "password": PASSWORD})

    assert response.status_code == 429
    assert b"Too many attempts" in response.content
    assert "_auth_user_id" not in client.session
