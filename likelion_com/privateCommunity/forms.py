from django import forms
from .models import Post
from ckeditor_uploader.widgets import CKEditorUploadingWidget

categories = [('자유게시판', '자유게시판') , ('공지게시판', '공지게시판'), ('질의응답게시판', '질의응답게시판')
            , ('모집게시판', '모집게시판'), ('정보게시판', '정보게시판'), ('앨범게시판', '앨범게시판')
]

class PostForm(forms.ModelForm):
    title = forms.CharField(label = '제목')
    content = forms.CharField(label='본문', widget=CKEditorUploadingWidget())
    category = forms.CharField(label='게시판 선택', widget=forms.Select(choices=categories))
    
    class Meta:
        model = Post
        fields = ['title' , 'category', 'content']
