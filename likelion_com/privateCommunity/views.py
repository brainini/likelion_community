from django.shortcuts import render, redirect
from .models import Post, Comment, Emotion, commentEmotion
from accounts.models import Profile
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator

# Create your views here.

def home(request):
    return render(request, 'privateCommunity/home.html')


def index(request):
    if request.method == 'GET': 
        posts = Post.objects.all().order_by('-created_at')            
        
        return render(
            request, 'privateCommunity/index.html',
            {'posts': posts,}
        )
    
    elif request.method == 'POST': 
        title = request.POST['title']
        content = request.POST['content']
        post = Post.objects.create(title=title, content=content, author=request.user)
        return redirect('privateCommunity:index') 

def new(request):
    return render(request, 'privateCommunity/index.html')

def show(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'privateCommunity/show.html', {'post':post})


def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete() 
    if request.method == 'DELETE' : 
        return JsonResponse({'postLikeCount': request.user.like_posts.count()});
    
    return redirect('privateCommunity:index') 

def update(request, id):
    if request.method == 'GET':
        post = Post.objects.get(id=id)
        return render(request, 'privateCommunity/update.html', {'post':post})
    
    elif request.method == 'POST':
        post = Post.objects.filter(id=id)
        post.update(title=request.POST['title'], content=request.POST['content'])
        post.first().tags.set(request.POST.getlist('tags'))

        return redirect('privateCommunity:show', id=id)


class CommentView:
    def create(request, id):
        content = request.POST['content']
        comment = Comment.objects.create(post_id=id, content=content, author=request.user)
        current_time = comment.created_at.strftime('%Y년 %m월 %d일 %-H:%M')

        post = Post.objects.get(id=id)
        return JsonResponse({
            'commentId': comment.id,
            'commentCount': post.comment_set.count(),
            'commentLikeCount': comment.like_users.count(), 
            'createdTime': current_time,
            'author': request.user.username 
        })
        
    def delete(request, id, cid):
        comment = Comment.objects.get(id=cid)
        comment.delete()
        post = Post.objects.get(id=id)
        return JsonResponse({'commentCount': post.comment_set.count()})

class EmotionView:
    def create(request, id):
        post = Post.objects.get(id=id)
        like_list = post.like_set.filter(user_id=request.user.id)
        if like_list.count() > 0:
            post.like_set.get(user=request.user).delete()
        else:
            Emotion.objects.create(user=request.user, post=post)
        return JsonResponse({
            'postEmotionOfUser': like_list.count(), 
            'postEmotionCount': post.like_set.count(), 
            'userEmotionCount': request.user.like_posts.count()
        })

class CommentEmotionView:
    def create(request, cid):
        comment = Comment.objects.get(id=cid)
        like_list = comment.commentemotion_set.filter(user_id=request.user.id)
        if like_list.count() > 0:
            comment.commentemotion_set.get(user=request.user).delete()
        else:
            commentEmotion.objects.create(user=request.user, comment=comment)
        return JsonResponse({'commentEmotionCount': comment.commentemotion_set.count()})


class board_NoticeList(ListView):
    model = Post
    paginate_by = 10
    template_name = 'privateCommunity/board_notice.html'
    context_object_name = 'board_notice'

    def get_queryset(self):
        board_notice = Post.objects.filter(category='공지게시판').order_by('-id') 
        return board_notice

    def get_context_data(self, **kwargs):
        context = super(board_NoticeList, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context


class board_AnnounceList(ListView):
    model = Post
    paginate_by = 10
    template_name = 'privateCommunity/board_announce.html'
    context_object_name = 'board_announce'

    def get_queryset(self):
        board_announce = Post.objects.filter(category='공고게시판').order_by('-id') 
        return board_announce
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context


class board_QnaList(ListView):
    model = Post
    paginate_by = 10
    template_name = 'privateCommunity/board_qna.html'
    context_object_name = 'board_qna'

    def get_queryset(self):
        board_qna = Post.objects.filter(category='질의응답게시판').order_by('-id') 
        return board_qna
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context



class board_ApplyList(ListView):
    model = Post
    paginate_by = 10
    template_name = 'privateCommunity/board_apply.html'
    context_object_name = 'board_apply'

    def get_queryset(self):
        board_apply = Post.objects.filter(category='모집게시판').order_by('-id') 
        return board_apply
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context



class board_FreeList(ListView):
    model = Post
    paginate_by = 10
    template_name = 'privateCommunity/board_free.html'
    context_object_name = 'board_free'

    def get_queryset(self):
        board_free = Post.objects.filter(category='자유게시판').order_by('-id') 
        return board_free
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context



class board_infoList(ListView):
    model = Post
    paginate_by = 10
    template_name = 'privateCommunity/board_info.html'
    context_object_name = 'board_info'

    def get_queryset(self):
        board_info = Post.objects.filter(category='정보게시판').order_by('-id') 
        return board_info
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range

        return context


