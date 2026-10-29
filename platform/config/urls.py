from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

CATEGORIES = [
    ("Web", "Exploit vulnerable web apps."),
    ("Crypto", "Break ciphers and encodings."),
    ("Forensics", "Find data hidden in files."),
    ("Reversing", "Pull secrets out of binaries."),
]

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="home.html", extra_context={"categories": CATEGORIES}),
        name="home",
    ),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
]
