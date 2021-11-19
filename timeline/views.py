from django.shortcuts import render,get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import PostForm,BrandSearchForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from .models import Post, Like,Item
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http.response import JsonResponse


def paginate_queryset(request, queryset, count):
    paginator = Paginator(queryset, count)
    page = request.GET.get('page')
    try:
        paginate_count = paginator.page(page)
    except PageNotAnInteger:
        paginate_count = paginator.page(1)
    except EmptyPage:
        paginate_count = paginator.page(paginator.num_pages)
    return paginate_count

def index(request):
    if(request.method == 'POST'): 
        form = BrandSearchForm(request.POST) 
        if 'button_all' in request.POST: 
            item_data = Item.objects.filter(display=True)
        elif 'button_yonex' in request.POST: 
            item_data = Item.objects.filter(brand_name='yonex',display=True)
        elif 'button_mizuno' in request.POST:
            item_data = Item.objects.filter(brand_name='mizuno',display=True)
        elif 'button_dunlop' in request.POST:
            item_data = Item.objects.filter(brand_name='dunlop',display=True)
        elif 'button_srixon' in request.POST:
            item_data = Item.objects.filter(brand_name='srixon',display=True)
        elif 'button_gosen' in request.POST:
            item_data = Item.objects.filter(brand_name='gosen',display=True)
    else:
        form = BrandSearchForm() 
        item_data = Item.objects.filter(display=True)
    
    paginate_count = paginate_queryset(request, item_data, 30)
    
    params = {
        'form' : form,
        'item_data' :  paginate_count.object_list,
        'page_obj' :  paginate_count,
    }
    return render(request, 'index.html', params)    

def post_list(request,item_url_name): 
    item_data = Item.objects.get(item_url_name = item_url_name)
    object_list = Post.objects.filter(item__item_url_name= item_url_name) 
    post_count = Post.objects.filter(item__item_url_name= item_url_name).count()
    paginate_count = paginate_queryset(request, object_list, 20)
    liked_list = []
    current_user = request.user
    if (current_user.is_authenticated):
        for post in object_list:
            liked = post.like_set.filter(user=request.user)
            if liked.exists():
                liked_list.append(post.pk)
                
    params = {
        'item_data':item_data,
        'object_list':paginate_count.object_list,
        'post_count':post_count,
        'page_obj':paginate_count,
        'liked_list' :liked_list,
    }
    return render(request, 'post_list.html',params)
    
@login_required
def LikeView(request):
    if request.method =="POST":
        post = get_object_or_404(Post, pk=request.POST.get('post_pk'))
        current_user = request.user
        liked = False
        like = Like.objects.filter(post=post, user=current_user)
        if like.exists():
            like.delete()
        else:
            like.create(post=post, user=current_user)
            liked = True
        
        context={
            'post_pk': post.pk,
            'liked': liked,
            'count': post.like_set.count(),
        }
    if request.is_ajax():
        return JsonResponse(context)
    
@login_required
def Liked_PostListView(request,pk):
    current_user = request.user
    like_data = Like.objects.filter(user=current_user)
    all_post = Post.objects.all()
    liked_list = []
    for post in all_post:
        liked = post.like_set.filter(user=request.user)
        if liked.exists():
            liked_list.append(post.pk)
            
    paginate_count = paginate_queryset(request, like_data, 50)
    
    params = {
        'object_list' :like_data,
        'liked_list' :liked_list,
        'page_obj':paginate_count,
    }
    return render(request, 'liked_post_list.html',params)
    

class MyPostListView(LoginRequiredMixin,generic.ListView):
    template_name = 'mypost_list.html'
    model = Post 
    paginate_by = 15
    
    def get_queryset(self):
        current_user = self.request.user
        return Post.objects.filter(author=current_user.id)

@login_required
def create_view(request,item_url_name): #レビュー作成関数
    if (request.method == "POST"):
        form = PostForm(request.POST,request.FILES) 
        if form.is_valid():
            post = form.save(commit=False)#フォームに入力された内容を一時的に保持
            post.author = request.user #postテーブルのauthorにリクエストされてきたログインユーザーpkを格納
            item_info = Item.objects.get(item_url_name= item_url_name) 
            post.item =  item_info
            post.save() 
            messages.success(request, 'レビューを作成しました。')
            return redirect('timeline:post_list',item_url_name = item_url_name)
    else:
        form = PostForm()
    return render(request, 'post_create.html', {'form': form})
    

class Post_EditView(LoginRequiredMixin,SuccessMessageMixin,generic.UpdateView): 
    model = Post
    slug_field = "Item__item_url_name"
    slug_url_kwarg = "Item__item_url_name"
    form_class = PostForm
    template_name = 'post_edit.html'
    success_message = 'レビューを変更しました。'

    def get_success_url(self):
        return reverse_lazy('timeline:post_list',kwargs={'item_url_name':self.object.item.item_url_name})


class MyPost_EditView(LoginRequiredMixin,SuccessMessageMixin,generic.UpdateView): 
    model = Post
    slug_field = "Item__item_url_name"
    form_class = PostForm
    template_name = 'mypost_edit.html'
    success_message = 'レビューを変更しました。'

    def get_success_url(self):
        return reverse_lazy('timeline:mypost_list',kwargs={'pk':self.request.user.pk})
       
       
class Post_DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    slug_field = "item_url_name"
    template_name = 'post_confirm_delete.html'
    def get_success_url(self):
        return reverse_lazy('timeline:post_list',kwargs={'item_url_name':self.object.item.item_url_name})    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == request.user: 
            messages.success(self.request, 'レビューを削除しました。')
        return super().delete(request, *args, **kwargs)
    
class MyPost_DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    slug_field = "item_url_name"
    template_name = 'mypost_confirm_delete.html'
    def get_success_url(self):
        return reverse_lazy('timeline:mypost_list',kwargs={'pk':self.request.user.pk})
        
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == request.user: 
            messages.success(self.request, 'レビューを削除しました。')
        return super().delete(request, *args, **kwargs)