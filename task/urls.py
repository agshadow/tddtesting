from django.urls import path

from task import views
from task.views import TaskListView

urlpatterns = [
    #path('', views.index, name='index'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('new/', views.new, name='new'),
    path("", TaskListView.as_view(), name='index')
]