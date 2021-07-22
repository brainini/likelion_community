from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Emotion, CommentEmotion, ReComment, ReCommentEmotion
from accounts.models import Profile
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator
from .forms import PostForm

# Create your views here.

def home(request):
    if request.method == 'POST':
        title = request.POST['title']
        category = request.POST['category']
        content = request.POST['content']
        post = Post.objects.create(author=request.user, title=title, category=category, content=content, view_count = 0)
        comments = post.comment_set.order_by('created_at')
        emotions = post.emotion_set
        return redirect('privateCommunity:show', id= post.id)
    else:
        posts = Post.objects.all()
        return render(request, 'privateCommunity/home.html', {'posts': posts})


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
    form = PostForm()
    context = {
        "form":form
    }
    return render(request, 'privateCommunity/new.html', context)

def show(request, id):

    post = Post.objects.get(id=id)
    post.view_count +=1
    post.save()
    comments = post.comment_set.order_by('created_at')
    emotions = post.emotion_set
    thanks_list = post.emotion_set.filter(type="thanks")
    best_list = post.emotion_set.filter(type="best")
    surprising_list = post.emotion_set.filter(type="surprising")
    funny_list = post.emotion_set.filter(type="funny")
    
    for comment in comments:
       
        comment_thanks_list = comment.commentemotion_set.filter(type="thanks")
        comment_best_list = comment.commentemotion_set.filter(type="best")
        comment_surprising_list = comment.commentemotion_set.filter(type="surprising")
        comment_funny_list = comment.commentemotion_set.filter(type="funny")
        comment.thanks_count = comment_thanks_list.count()
        comment.best_count = comment_best_list.count()
        comment.surprising_count = comment_surprising_list.count()
        comment.funny_count = comment_funny_list.count()
        comment.emotion_count = comment.best_count + comment.thanks_count + comment.surprising_count + comment.funny_count
        recomments = comment.recomment_set.all()
        comment.recomment_list = recomments
        for recomment in recomments:
            recomment_thanks_list = recomment.recommentemotion_set.filter(type="thanks")
            recomment_best_list = recomment.recommentemotion_set.filter(type="best")
            recomment_surprising_list = recomment.recommentemotion_set.filter(type="surprising")
            recomment_funny_list = recomment.recommentemotion_set.filter(type="funny")
            recomment.thanks_count = recomment_thanks_list.count()
            recomment.best_count = recomment_best_list.count()
            recomment.surprising_count = recomment_surprising_list.count()
            recomment.funny_count = recomment_funny_list.count()
            recomment.emotion_count = recomment.best_count + recomment.thanks_count + recomment.surprising_count + recomment.funny_count
    comment_count = post.comment_set.count()
    for comment in post.comment_set.all():
        comment_count += comment.recomment_set.count()

    context = {
    'post':post,
    'comments':comments,
    'emotions': emotions,
    'postThanksCount': thanks_list.count(),
    'postBestCount': best_list.count(),
    'postSurprisingCount': surprising_list.count(),
    'postFunnyCount': funny_list.count(),
    'commentCount': comment_count
    }

    return render(request, 'privateCommunity/show.html', context)


def delete(request, id):
    post = Post.objects.get(id=id)
    post.delete() # 선택된 모델 인스턴스를 삭제하는 query 함수입니다.
    return redirect('privateCommunity:home')

def edit(request, id):
    
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid(): # 잘입력된지 체크
            post = form.save(commit=False)
            post.save() # 저장하기
            comments = post.comment_set.order_by('created_at')
            emotions = post.emotion_set
            return render(request, 'privateCommunity/show.html', {'post':post, 'comments':comments, 'emotions':emotions})

    # 빈 페이지 띄워주는 기능 -> GET
    else :
        form = PostForm(instance=post)
        return render(request, 'privateCommunity/edit.html', {'post':post,'form':form})


class CommentView:
    def create(request, id):
        content = request.POST['content']
        comment = Comment.objects.create(post_id=id, content=content, author=request.user)
        post = Post.objects.get(id=id)
        comment_count = post.comment_set.count()
        for comment in post.comment_set.all():
            comment_count += comment.recomment_set.count()
        return JsonResponse({
            'commentId': comment.id,
            'author': comment.author.username,
            'created_at': comment.created_at.strftime("%Y년 %m월 %d일 %-H:%M".encode('unicode-escape').decode()).encode().decode('unicode-escape'),
            'commentCount': comment_count
        })
        
    def delete(request, id, cid):
        comment = Comment.objects.get(id=cid)
        comment.delete()
        post = Post.objects.get(id=id)
        comment_count = post.comment_set.count()
        for comment in post.comment_set.all():
            comment_count += comment.recomment_set.count()
        return JsonResponse({
            'commentCount': comment_count
        })


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


class ReCommentView:
    def create(request, id, cid):
        content = request.POST['content']
        recomment = ReComment.objects.create(comment_id=cid, content=content, author=request.user)
        post = Post.objects.get(id=id)
        comment_count = post.comment_set.count()
        for comment in post.comment_set.all():
            comment_count += comment.recomment_set.count()
        return JsonResponse({
            'recommentId': recomment.id,
            'author': recomment.author.username,
            'created_at': recomment.created_at.strftime("%Y년 %m월 %d일 %-H:%M".encode('unicode-escape').decode()).encode().decode('unicode-escape'),
            'commentCount': comment_count
        })
        
    def delete(request, id, cid, rcid):
        recomment = ReComment.objects.get(id=rcid)
        recomment.delete()
        post = Post.objects.get(id=id)
        comment_count = post.comment_set.count()
        for comment in post.comment_set.all():
            comment_count += comment.recomment_set.count()
        return JsonResponse({
            'commentCount': comment_count
        })

class EmotionView:
    def create(request, id, type):
        post = Post.objects.get(id=id)
        emotion_list = post.emotion_set.filter(user_id=request.user.id,type=type)
        if emotion_list.count() > 0:
            emotion_list.delete()
        else:
            Emotion.objects.create(user=request.user, post=post, type=type)
        thanks_list = post.emotion_set.filter(type="thanks")
        best_list = post.emotion_set.filter(type="best")
        surprising_list = post.emotion_set.filter(type="surprising")
        funny_list = post.emotion_set.filter(type="funny")
        return JsonResponse({
            'postThanksCount': thanks_list.count(),
            'postBestCount': best_list.count(),
            'postSurprisingCount': surprising_list.count(),
            'postFunnyCount': funny_list.count(),
        })

class CommentEmotionView:
    def create(request, id, cid, type):
        comment = Comment.objects.get(id = cid)
        comment_emotion_list = comment.commentemotion_set.filter(user_id=request.user.id, type=type)
        if comment_emotion_list.count() > 0:
            comment_emotion_list.delete()
        else:
            CommentEmotion.objects.create(user=request.user, comment=comment, type=type)
        thanks_list = comment.commentemotion_set.filter(type="thanks")
        best_list = comment.commentemotion_set.filter(type="best")
        surprising_list = comment.commentemotion_set.filter(type="surprising")
        funny_list = comment.commentemotion_set.filter(type="funny")
        return JsonResponse({
            'thanksCount': thanks_list.count(),
            'bestCount': best_list.count(),
            'surprisingCount': surprising_list.count(),
            'funnyCount': funny_list.count(),
        })

class RecommentEmotionView:
    def create(request, id, cid, rcid, type):
        recomment = ReComment.objects.get(id = rcid)
        recomment_emotion_list = recomment.recommentemotion_set.filter(user_id=request.user.id, type=type)
        if recomment_emotion_list.count() > 0:
            recomment_emotion_list.delete()
        else:
            ReCommentEmotion.objects.create(user=request.user, recomment=recomment, type=type)
        thanks_list = recomment.recommentemotion_set.filter(type="thanks")
        best_list = recomment.recommentemotion_set.filter(type="best")
        surprising_list = recomment.recommentemotion_set.filter(type="surprising")
        funny_list = recomment.recommentemotion_set.filter(type="funny")
        return JsonResponse({
            'thanksCount': thanks_list.count(),
            'bestCount': best_list.count(),
            'surprisingCount': surprising_list.count(),
            'funnyCount': funny_list.count(),
        })




