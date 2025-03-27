from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('user-create',views.createUser),
    path('create-manager', views.createManager),
    path('create-employee',views.createEmployee),
    path('logoutuser', views.logoutUser),
    path('login-manager', views.loginManager,name='loginmanager'),
    path('loginuser', views.loginUser,name='loginuser'),
    path('all-emp', views.allEmp),
    path('make-task', views.createUserTask),
    path('managertouser', views.managerToUserTask),
    path('managertouser/<str:employee_id>', views.managerToUserTask),
    path('show-all-task', views.allManagerTask),
    path('delete-employee/<int:id>', views.deleteEemployee),
    path('find-user-tasks', views.filterUserTask),
    path('task-update',views.taskUpdate)
]