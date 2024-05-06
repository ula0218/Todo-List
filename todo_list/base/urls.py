from django.urls import path
from .views import TaskList,TaskDetail,TaskCreate,TaskUpdate,TaskDelete,CustomLoginView,RegisterPage
from django.contrib.auth.views import LogoutView


app_name = 'tasks'

urlpatterns = [
    path('',TaskList.as_view(),name='tasks'),
    path('register/',RegisterPage.as_view(),name='register'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page = 'tasks:login' ),name='logout'),
    path('task-create/',TaskCreate.as_view(),name='task-create'),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name='task-update'),
    path('task-delete/<int:pk>/',TaskDelete.as_view(),name='task-delete'),
    path('<int:pk>/',TaskDetail.as_view(),name='task'),
]