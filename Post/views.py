from django.shortcuts import render,redirect
from django.db.models import Count
from django.core.paginator import Paginator
from django.db.models import Q  
from .models import *
from django.contrib import messages
import uuid
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import logout,authenticate,login,logout

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




def signup(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # print(f'fname : {fname} \n lname : {lname} \n email : {email} \n password : { password} \n username : {username} \n')

        user_check = User.objects.filter(username=username).first()
        email_check = User.objects.filter(email=email).first()

        if user_check is not None:
            messages.success(request,"Username is already taken.Please choose another name.")
            return redirect("/signup/")

        if email_check is not None:
            messages.success(request,"Email is already taken. Pleese choose another email")
            return redirect("/signup/")       

        user = User(username=username,first_name=fname,last_name=lname,email=email)
        user.set_password(password)

        user.save()
        token = uuid.uuid4()
        profile = Profile(user=user,token=token)
        profile.save()
        # send_mail(email,token)
        messages.success(request, "Please check your email to verify your email account")

    return render(request,"signup.html")


def userLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if user is not None:
            profle = Profile.objects.filter(user=user).first()
            if profle.is_verified:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("/")
                else:
                    messages.success(request, "Invalid username or password.")
                    return redirect("/login/")
            else:
                messages.success(request, "Email is not verified.")
                return redirect("/login/")
        else:
            messages.success(request, "Invalid Username.")
            return redirect("/login/")


    return render(request, "login.html")


def send_email(email,token):
    subject = 'SHEBI BLOG ! PLEASE VERIFY YOUR EMAIL. '
    body = f'Paste a link into browser to verify your email http://127.0.0.1:8000/verify/{token}/ '
    email = EmailMessage(
        subject, #subject
        body, # body
        settings.EMAIL_HOST_USER,#sender
        [email] #recever
    )
    email.fail_silently=False
    email.send()


def verify(request,auth_token):
    profile_obj = Profile.objects.filter(token=auth_token).first()

    if profile_obj is not None:
        profile_obj.is_verified = True
        profile_obj.save()
        messages.success(request, "Your email is verified successfully now you can LOGIN.")
        return redirect("/login/")
    else:
        messages.success(request, "Your email is not verified ! Try Again Please .")
        return redirect("/signup/")


def userLogout(request):
    logout(request)
    return redirect('/login/')
    