from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm

# Create your views here.

def post_list(request):
    # orders by date
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'blog/blogposts.html', {'posts': posts})

def post_top5(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by("-views")[:2]
    return render(request, 'blog/blogposts.html', {'posts': posts})
    
def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    post.views += 1
    post.save()
    return render(request, "blog/blogdetail.html",{'post':post})

def new_post(request):
    form = BlogPostForm()
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect(post_detail, post.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/blogpostform.html', {'form': form})

