from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.contrib.auth import (login, logout)
from projects.models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Avg

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


# Create your views here.

@login_required
def home_page(request):  # home page view
    top_5projects = []
    admin_choice = []
    latest_projects = []
    # Categories
    categories = Categories.objects.all()
    # Top rated binding with their images
    top_rated = Rating.objects.values('project_id').annotate(rates=Avg('rating')).order_by('-rates')[:5]
    for i in top_rated:
        project = Projects.objects.get(pk=i['project_id'])
        images = Images.objects.filter(project_id=i['project_id'])
        top_5projects.append({'project': project, 'images': images})

    # Admin choosen projects binding with their images
    admin_choice_query = Choosen_by_Admin.objects.all()[:5]
    for i in admin_choice_query:
        images = Images.objects.filter(project_id=i.id)
        admin_choice.append({'project': i, 'images': images})

    # Latest Added projects
    latest_projects_query = Projects.objects.order_by('-id')[:5]
    for i in latest_projects_query:
        images = Images.objects.filter(project_id=i.id)
        latest_projects.append({'project': i, 'images': images})
    context = {'top5': top_5projects, 'admin_choice': admin_choice,
               'latest_projects': latest_projects, 'categories': categories}
    return render(request, 'home.html', context)


@login_required
def profile_page(request, username):
    user = User.objects.get(username=username)
    id = user.id
    addtionalinfo = Profile.objects.get(user_id=id)
    user_project = Projects.objects.filter(user_id=id)
    categories = Categories.objects.all()

    if user:
        context = {
            'userinfo': user,
            'addtionalinfo': addtionalinfo,
            'userproject': user_project,
            'categories': categories
        }
        return render(request, 'profile.html', context)
    else:
        return HttpResponse("No User Available")


@login_required
def editprofile(request, id):
    user = User.objects.filter(pk=id).update(username=request.POST['username'], email=request.POST['email'])
    addtionalinfo = Profile.objects.filter(user_id=id).update(country=request.POST['country'],
                                                              phone=request.POST['phone'],
                                                              social_media=request.POST['social_media'],
                                                              birth=request.POST['birth'])
    ur = User.objects.get(pk=id)
    return redirect(profile_page, username=ur.username)


def Mylogin(request):
    if request.method == 'POST':
        form = userLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('/user/home')
            else:
                return render(request, "login.html", {"form": form, "msg": "Not User"})
    else:
        form = userLogin()
    return render(request, "login.html", {"form": form})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        form2 = UserProfile(request.POST, request.FILES)
        if form.is_valid() and form2.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            profile = form2.save(commit=False)
            profile.is_active = 0
            current_user = User.objects.get(username=username)
            profile.user = current_user
            profile.save()

            """ 
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('activation.html', {
                'user': profile,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(profile.pk)),
                'token': account_activation_token.make_token(profile),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')"""
            return redirect('/user/login')
    else:
        form = UserRegisterForm()
        form2 = UserProfile()
    return render(request, 'register.html', {'form': form, 'form2': form2})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = profile_page.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = 1
        user.save()
        login(request, user)
        return redirect('/user/login')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def Mylogout(request):
    logout(request)
    return redirect('login')
