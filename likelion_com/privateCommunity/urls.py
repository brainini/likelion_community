from django.urls import path
from privateCommunity import views

app_name = 'privateCommunity'
urlpatterns = [
    path('', views.home, name='home'), # 'localhost:8000/community/'
    path('new/', views.new, name='new'),
    path('<int:id>/', views.show, name='show'),
    path('notice/', views.board_NoticeList.as_view(), name='board_notice'),
    path('announce/', views.board_AnnounceList.as_view(), name='board_announce'),
    path('qna/', views.board_QnaList.as_view(), name='board_qna'),
    path('apply/', views.board_ApplyList.as_view(), name='board_apply'),
    path('free/', views.board_FreeList.as_view(), name='board_free'),
    path('info/', views.board_infoList.as_view(), name='board_info'),
]


