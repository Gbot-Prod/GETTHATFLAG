from django.urls import reverse


def test_home_page_renders(admin_client):
    response = admin_client.get(reverse("home"))

    assert response.status_code == 200
    assert b"GETTHATFLAG" in response.content
    assert b"htmx.min.js" in response.content
