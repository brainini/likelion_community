from django.urls import path
from guestbook import views

app_name = 'guestbook'
urlpatterns = [
path('list/', views.list, name='list'),
path('write/', views.write, name='write'),
path('delete/<int:id>', views.delete, name='delete'),
]