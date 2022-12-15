from django.urls import path
from todoweb import views

urlpatterns = [
    path("register/",views.RegisterView.as_view(),name="signup"),
    path('login/',views.LoginView.as_view(),name="signin"),
    path("index/",views.IndexView.as_view(),name="home"),
    path('todoss/alll/',views.TodoListView.as_view(),name="alltodos"),
    path('todo/add/',views.TodoCreateView.as_view(),name="addtodos"),
    path('todoos/<int:id>/',views.TodoDetail.as_view(),name="todos-details"),
    path('todos/<int:id>/remove/',views.todo_delete_view,name="todos-delete"),
]
