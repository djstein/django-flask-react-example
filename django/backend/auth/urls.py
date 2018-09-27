from django.urls import path, re_path
from auth.views import users

urlpatterns = (
    path("users/", users, name="users"),
    path("users/<id>/", users, name="users"),
)
