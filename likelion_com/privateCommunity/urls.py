from django.urls import path
from privateCommunity import views


app_name = 'privateCommunity'
urlpatterns = [
    path('', views.home, name='home'), # 'localhost:8000/community/'
    path('posts/new/', views.new, name= 'new'),
    path('posts/<int:id>/', views.show, name= 'show' ),
    path('posts/<int:id>/edit', views.edit, name='edit'),
    path('posts/<int:id>/delete/', views.delete, name='delete'),
    path('posts/<int:id>/comments/', views.CommentView.create, name='comment_create'),
    path('posts/<int:id>/comments/<int:cid>/', views.ReCommentView.create, name='recomment_create'),
    path('posts/<int:id>/comments/<int:cid>/delete', views.CommentView.delete, name='comment_delete'),
    path('posts/<int:id>/comments/<int:cid>/delete/<int:rcid>', views.ReCommentView.delete, name='recomment_delete'),
    path('posts/<int:id>/emotion/<str:type>', views.EmotionView.create, name='emotion'),
    path('posts/<int:id>/comments/<int:cid>/commentEmotion/<str:type>', views.CommentEmotionView.create, name='commentEmotion'),
    path('posts/<int:id>/comments/<int:cid>/<int:rcid>/reCommentEmotion/<str:type>', views.CommentEmotionView.create, name='commentEmotion'),
]