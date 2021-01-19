from django.shortcuts import render,get_object_or_404,redirect,Http404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from blog.models import Post,Comment
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator,EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView,ListView,
                                DetailView,UpdateView,
                                DeleteView,CreateView)

class SafePaginator(Paginator):
    def validate_number(self,number):
        try:
            return super(SafePaginator,self).validate_number(number)
        except EmptyPage:
            if number>0:
                return self.num_pages
            else:
                raise
class AboutView(TemplateView):
    template_name='about.html'

class PostListView(ListView):
    paginator_class=SafePaginator
    model=Post
    context_object_name='posts'
    paginate_by=4
    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    
class PostDetailView(DetailView,LoginRequiredMixin):
    model=Post
    context_object_name='post'
    login_url = reverse_lazy('login')
    redirect_field_name = '/'

class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    form_class=PostForm
    login_url = reverse_lazy('login')
    redirect_field_name='/'
    
    raise_exception = False
    # def handle_no_permission(self):
    #     if self.raise_exception:
    #         raise PermissionDenied(self.get_permission_denied_message())
    #     return redirect('login')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostCreateView, self).form_valid(form)

class PostUpdateView(UpdateView,LoginRequiredMixin):
    model=Post
    form_class=PostForm
    login_url = reverse_lazy('login')
    redirect_field_name='blog/post_detail.html'

class PostDeleteView(DeleteView,LoginRequiredMixin):
    model=Post
    success_url=reverse_lazy('post_list')

   

class DraftListView(ListView,LoginRequiredMixin):
    model=Post
    redirect_field_name='login'
    template_name='blog/post_drafts_list.html'
    login_url=reverse_lazy('login')
    context_object_name='posts'

    
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')

###########################################
############################################
@login_required
def publish_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)



@login_required
def add_comment_to_post(request,pk):
    post=get_object_or_404(Post,pk=pk)
    if request.method=='POST':
        form=CommentForm(request.POST)
        if form.is_valid():
            comment=form.save(commit=False)
            comment.post=post
            comment.author=request.user
            comment.save()
            return redirect('post_detail',pk=pk)
    else:
        form=CommentForm()
        return render(request,'blog/comment_form.html',{'form':form})
    
@login_required
def comment_approve(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment=get_object_or_404(Comment,pk=pk)
    post_pk=comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

