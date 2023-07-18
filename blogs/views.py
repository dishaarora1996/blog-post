from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Blog, Category, Comment
from django.db.models import Q

# Create your views here.


def posts_by_category(request, category_id):
    # fetch the posts that belong to the category with id category id

    posts = Blog.objects.filter(status="Published", category=category_id)
    try:
        category = Category.objects.get(id=category_id)
        print(f"*********** {category}")
    except:
        return redirect('home')
    context = {
        'posts': posts,
        'category': category
    }
    print(f"*********** {posts}")
    return render(request, 'posts_by_category.html', context)


def blogs(request, blog_slug):
    print("slug", blog_slug)
    single_blog = get_object_or_404(Blog, slug=blog_slug, status="Published")

    # comments
    if request.method == 'POST':
        comment = Comment.objects.create(blog= single_blog, comment= request.POST['comment'], user= request.user)
        comment.save()
        return HttpResponseRedirect(request.path_info)

    comments = Comment.objects.filter(blog=single_blog)
    comment_count = comments.count()

    context = {
        'single_blog': single_blog,
        'comments': comments,
        'comment_count': comment_count
    }
    return render(request, 'blogs.html', context)


def search(request):
    print("keyword")
    keyword = request.GET.get('keyword')
    print("keyword", keyword)
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status="Published")
    print("blogs", blogs)

    context = {
        'posts': blogs,
        'keyword': keyword
    }

    return render(request, 'search.html', context)
