from django.shortcuts import render,redirect
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q  
from .models import *
# Create your views here.


def index(request):
    searchtext = request.GET.get('searchtext')
    if searchtext is None:
        searchtext = ""
    print(searchtext)
    posts = Post.objects.filter(Q(category__name__icontains=searchtext) | Q(title__icontains=searchtext)|Q(author__user__username=searchtext)).order_by('-id')
    # PAGINATOR LOGIC 
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    post_obj = paginator.get_page(page_number)
    print("#######################")
    print(post_obj.has_next())
    print("####################")
    #LATEST POST 
    latest_posts = Post.objects.all().order_by('-id')[:5]
    # categories = Category.objects.annote(number_of_post=)
    categories = Category.objects.annotate(number_of_post=Count('post'))


    tags = Tag.objects.all()
    context={
        'posts':posts,
        'post_obj':post_obj,
        'latest_posts':latest_posts,
        'categories':categories,
        'tags':tags,
    }
    return render(request,"index.html",context)


def detail(request,pk):
    # Add POST COMMENTS LOGIC
    if request.method =="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        website = request.POST.get('website')
        body  = request.POST.get('body')
        mypost = Post.objects.get(id=pk)

        comment = Comment(username=name,email=email,website=website,body=body,post=mypost)

        comment.save()




    mypost = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post__id = pk)
    count_comments = comments.count()
    print(count_comments)
    print(comments)
    latest_posts = Post.objects.all().order_by('-id')[:5]
    # categories = Category.objects.annote(number_of_post=)
    categories = Category.objects.annotate(number_of_post=Count('post'))

    tags = Tag.objects.all()
    context={
        'mypost':mypost,
        'latest_posts':latest_posts,
        'categories':categories,
        'tags':tags,
        'comments':comments,
        'count_comments':count_comments,
    }
    return render(request,"detail.html",context)