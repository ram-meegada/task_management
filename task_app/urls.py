from django.urls import path
from .views import *


urlpatterns = [
    path('login/', LoginView.as_view(), name='google_login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('tasks/list/', TasksListView.as_view(), name='task_list'),

    path('task/create/', CreateTaskView.as_view(), name='task_create'),
    path('task/edit/<int:id>/', EditTaskView.as_view(), name='task_edit'),
    path('task/delete/<int:id>/', DeleteTaskView.as_view(), name='task_delete'),
]
