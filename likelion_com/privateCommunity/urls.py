from django.urls import path
from privateCommunity import views

urlpatterns = [
    path('', views.home, name='home'), # 'localhost:8000/community/'
]