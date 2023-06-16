from django.shortcuts import render
from .models import *
from .forms import CommentForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

# Create your views here.
def home_view(request):
    queryset = BlogPost.objects.filter(status='published').order_by('-created')
    per_page = 3
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    template_name = 'index.html'
    context = {'posts': posts}
    return render(request, template_name, context)

def About(request):
    templates_name='blog/about.html'
    contex = {}
    return render(request, templates_name, contex )

def Blog(request):
    queryset = BlogPost.objects.filter(status = 'published').order_by('-created')
    per_page = 3
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    template_name= 'blog/blog.html'
    context = {'posts': posts, }
    return render(request, template_name, context)


# def single_post(request, slug):
#     post = get_object_or_404(BlogPost, slug=slug)
#     template_name = 'blog/single.html'
#     context = {'post':post}
#     return render(request, template_name, context)

def single_post(request, slug):
    template_name = 'blog/single.html'
    post = get_object_or_404(BlogPost, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    context = {'posts': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form}
    return render(request, template_name, context)
