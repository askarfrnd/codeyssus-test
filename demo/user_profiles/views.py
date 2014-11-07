from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q

from .utils import create_random_string
from .forms import AuthenticationForm, UserRegistrationForm, ContentUploadForm, CaptionForm
from .models import UserProfile, Photo, Audio, Video


def home(request):
    temp_dict = {}
    reg_form = UserRegistrationForm()
    login_form = AuthenticationForm()
    if request.user.is_authenticated():
        if request.user.is_staff:
            return HttpResponseRedirect('/admin')
        else:
            return HttpResponseRedirect('/dashboard')
    if request.POST:
        reg_form = UserRegistrationForm(request.POST)
        if reg_form.is_valid():
            user_profile_obj = reg_form.save(commit=False)
            user_obj = User.objects.create_user(username=create_random_string(),
                                                email=request.POST['email'], password=request.POST['password'])
            user_profile_obj.user = user_obj
            user_profile_obj.registration_type = "NORMAL"
            user_profile_obj.save()

            User.objects.filter(~Q(id=user_obj.id) & Q(email=user_obj.email)).delete()
            messages.success(request, "Thank you for registering. You may now login.")
            user_login = authenticate(username=request.POST['email'], password=request.POST['password'])
            if user_login:
                login(request, user_login)
                return HttpResponseRedirect('/email/verify/')
            else:
                temp_dict['error_message'] = "Invalid Credentials."
    temp_dict['form'] = reg_form
    temp_dict['login_form'] = login_form
    return render_to_response(
        'home.html',
        temp_dict, context_instance=RequestContext(request))


def login_user(request):
    if request.user.is_authenticated():
        if request.user.is_staff:
            return HttpResponseRedirect('/admin')
        else:
            return HttpResponseRedirect('/dashboard')

    temp_dict = {}
    form = AuthenticationForm()
    if request.POST:
        form = AuthenticationForm(request.POST)
        email = request.POST['username']
        password = request.POST['password']
        user_login = authenticate(username=email, password=password)
        if user_login:
            login(request, user_login)
            return HttpResponseRedirect('/dashboard/')
        else:
            temp_dict['error_message'] = "Invalid Credentials."

    temp_dict['form'] = form
    return render_to_response(
        'login.html',
        temp_dict, context_instance=RequestContext(request))


@login_required()
def dashboard(request):
    if request.user.is_staff:
        return HttpResponseRedirect('/admin')

    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except:
        if request.user.first_name != "":
            user_profile = UserProfile(name=request.user.first_name, user=request.user, registration_type="SOCIAL").save()
        else:
            user_profile = UserProfile(name=request.user.username, user=request.user, registration_type="SOCIAL").save()

    temp_dict = {}
    temp_dict['user_profile'] = user_profile
    return render_to_response(
        'dashboard.html',
        temp_dict, context_instance=RequestContext(request))


@login_required()
def user_profile(request):
    user_profile = request.user.user_profile
    temp_dict = {}
    print user_profile.caption
    caption_form = CaptionForm()
    form = ContentUploadForm()
    temp_dict['photos'] = Photo.objects.filter(user_profile=user_profile)
    temp_dict['audios'] = Audio.objects.filter(user_profile=user_profile)
    temp_dict['videos'] = Video.objects.filter(user_profile=user_profile)
    if request.POST:
        if request.FILES:
            print request.POST, request.FILES
            form = ContentUploadForm(request.POST, request.FILES)
            if 'photo_submit' in request.POST:
                photo_obj = Photo()
                photo_obj.user_profile = user_profile
                photo_obj.file_path = request.FILES['file']
                photo_obj.save()
            if 'audio_submit' in request.POST:
                audio_obj = Audio()
                audio_obj.user_profile = user_profile
                audio_obj.file_path = request.FILES['file']
                audio_obj.save()
            if 'video_submit' in request.POST:
                video_obj = Video()
                video_obj.user_profile = user_profile
                video_obj.file_path = request.FILES['file']
                video_obj.save()
        else:
            user_profile.caption = request.POST['caption']
            user_profile.save()
    temp_dict['form'] = form
    temp_dict['caption_form'] = caption_form
    temp_dict['user_profile'] = user_profile
    return render_to_response(
        'profile.html',
        temp_dict, context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')