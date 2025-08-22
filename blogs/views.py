from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from . models import Blogs, Category, Comment
from django.db.models import Q
from django.http import HttpResponseRedirect

# Create your views here.
def posts_by_category(request, category_id):
    try:
        posts = Blogs.objects.filter(category=category_id, status='published')
        category = get_object_or_404(Category, pk=category_id)
        
        context = {
            'posts': posts,
            'category': category,
        }
        return render(request, 'posts_by_category.html', context)
    except Exception as e:
        print(f"Error: {e}")  # This will print to your console
        return render(request, '404.html', status=500)


# blogs ------------------------------->

def blogs(request, slug):
  single_post = get_object_or_404(Blogs, slug=slug, status='published')

  if request.method=="POST":
      comment=Comment()
      comment.user=request.user
      comment.blog=single_post
      comment.comment=request.POST['comment']
      comment.save()
      return HttpResponseRedirect(request.path_info)
  
  comments = Comment.objects.filter(blog=single_post)
  comment_count = comments.count()  
  context = {
    'single_post':single_post,
    'comments':comments,
    'comment_count':comment_count
  }
  return render(request, 'blogs.html', context)


# search-------------------->

def search(request):
    keyword= request.GET.get('keyword')
    blog = Blogs.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='published')
    content = {
        'blogs':blogs
    }
    return render(request, 'search.html', content)
