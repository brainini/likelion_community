from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model): # 모델 클래스명은 단수형을 사용 (Posts(x) Post(O))
    # id는 자동 추가
    author = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    title = models.CharField(max_length=256)
    category = models.CharField(max_length=256)
    content = models.CharField(max_length=256, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(blank=True, null=True)
    view_count = models.IntegerField(blank=True, null=True)
    emotion_users = models.ManyToManyField(User, blank=True, related_name='emotion_posts', through='Emotion')

    def update_date(self): # 나중에 수정할 때 사용
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title

# 대댓글 view 구현시 참조
# https://velog.io/@suasue/Django-%EC%9D%B8%EC%8A%A4%ED%83%80%EA%B7%B8%EB%9E%A8-%ED%81%B4%EB%A1%A0-%EC%BD%94%EB%94%A910-%EB%8C%80%EB%8C%93%EA%B8%80-%EB%8B%AC%EA%B8%B0
class Comment(models.Model):
    author = models.ForeignKey(User, null=True, on_delete= models.CASCADE)
    content = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    emotion_users = models.ManyToManyField(User, blank=True, related_name='emotion_comments', through='CommentEmotion')

    def __str__(self):
        return f'[post: {self.post}] {self.content}'


class Emotion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.CharField(max_length= 20)
    created_at = models.DateTimeField(default=timezone.now)

class commentEmotion(models.Model):  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Comment, on_delete=models.CASCADE)
    type = models.CharField(max_length= 20)
    created_at = models.DateTimeField(default=timezone.now)