from django.contrib.auth.views import LoginView
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import TaskListView

urlpatterns = [
    path("", TaskListView.as_view(), name="home"),
    path("", views.home, name="home"),
    path("tags/", views.tag_list, name="tag_list"),
    path("add_task/", views.add_task, name="add_task"),
    path("add_tag/", views.add_tag, name="add_tag"),
    path("update_task/<int:pk>/", views.update_task, name="update_task"),
    path("delete_task/<int:pk>/", views.delete_task, name="delete_task"),
    path("toggle_task_status/<int:pk>/", views.toggle_task_status, name="toggle_task_status"),
    path("update_tag/<int:pk>/", views.update_tag, name="update_tag"),
    path("delete_tag/<int:pk>/", views.delete_tag, name="delete_tag"),
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="tasks/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name="tasks/logout.html"), name="logout"),
]
