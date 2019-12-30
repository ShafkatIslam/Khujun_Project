import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.contrib import messages
from django.db.models import Q
from .forms import AlbumForm, SongForm, UserForm, TeacherRegistrationForm , GuardianRegistrationForm, TeacherProfileForm, GuardianProfileForm, TuitionInfoForm, TeacherRatingForm
from .models import TeacherRegistration,GuardianRegistration
from .models import Album, Song, TeacherProfile, GuardianProfile, TuitionInfo, TeacherRating, Subscription
from django.db.models import Avg
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'Khujun/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'Khujun/create_album.html', context)
            album.save()
            return render(request, 'Khujun/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'Khujun/create_album.html', context)


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.song_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'Khujun/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.audio_file = request.FILES['audio_file']
        file_type = song.audio_file.url.split('.')[-1]
        file_type = file_type.lower()
        if file_type not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'Khujun/create_song.html', context)

        song.save()
        return render(request, 'Khujun/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'Khujun/create_song.html', context)


def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.filter(user=request.user)
    return render(request, 'Khujun/index.html', {'albums': albums})


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'Khujun/detail.html', {'album': album})


def detail(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'Khujun/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'Khujun/detail.html', {'album': album, 'user': user})


def favorite(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    try:
        if song.is_favorite:
            song.is_favorite = False
        else:
            song.is_favorite = True
        song.save()
    except (KeyError, Song.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def index(request):
        return render(request, 'Khujun/login.html')


def home(request):
    user = request.user
    if user.is_active:
        if TeacherRegistration.objects.filter(user=user):
            context = {
                'teacher': 'teacher',
            }
        elif GuardianRegistration.objects.filter(user=user):
            context = {
                'guardian': 'guardian',
            }
        return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/home.html')


def teacher_notification(request):
    user = request.user
    if user.is_active:
        if TeacherRegistration.objects.filter(user=user):
            login(request, user)
            notifications = TeacherProfile.objects.filter(user=user).get()
            notify = notifications.notification
            TeacherProfile.objects.filter(user=user).update(notifications=0)
            if (notify == 0):
                messages.info(request, 'আপনার নতুন কোনো নোটিফিকেশন নেই')
                return render(request, 'Khujun/teacher_notification.html')
            else:
                profiles = TuitionInfo.objects.filter(teacher_username=user).all().order_by('id').reverse()
                context = {
                    'profiles': profiles,
                }
                return render(request, 'Khujun/teacher_notification.html', context)
        else:
            context = {
                'guardian': 'guardian',
            }
            return render(request, 'Khujun/main_login.html', context)

    else:
        return render(request, 'Khujun/main_login.html')

def guardian_notification(request):
    user = request.user
    if user.is_active:
        if GuardianRegistration.objects.filter(user=user):
            login(request, user)
            notifications = GuardianProfile.objects.filter(user=user).get()
            notify = notifications.notification
            GuardianProfile.objects.filter(user=user).update(notifications=0)
            if (notify == 0):
                messages.info(request, 'আপনার নতুন কোনো নোটিফিকেশন নেই')
                return render(request, 'Khujun/guardian_notification.html')
            else:
                profiles = TuitionInfo.objects.filter(user=user).all().order_by('id').reverse()
                context = {
                    'profiles': profiles,
                }
                return render(request, 'Khujun/guardian_notification.html', context)
        else:
            context = {
                'teacher': 'teacher',
            }
            return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/main_login.html')



def mainreg(request):
    return render(request, 'Khujun/main_register.html')

def mainlogin(request):
    user = request.user
    if user.is_active:
        if TeacherRegistration.objects.filter(user=user):
            context = {
                'teacher': 'teacher',
            }
        elif GuardianRegistration.objects.filter(user=user):
            context = {
                'guardian': 'guardian',
            }
        return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/main_login.html')

def logout_user(request):
    if request.method == "POST":
        logout(request)
        form = UserForm(request.POST or None)
        context = {
            "form": form,
        }
        return render(request, 'Khujun/main_login.html', context)
    else:
        user = request.user
        if user.is_active:
            if TeacherRegistration.objects.filter(user=user):
                context = {
                    'teacher': 'teacher',
                }
            elif GuardianRegistration.objects.filter(user=user):
                context = {
                    'guardian': 'guardian',
                }
            return render(request, 'Khujun/main_login.html', context)
        else:
            return render(request, 'Khujun/main_login.html')
def subscribe(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']

        subcription = Subscription(name = name,email = email)
        subcription.save()
        messages.info(request, 'আপনার সাবস্ক্রিপশন সম্পন্ন হয়েছে')
        return render(request, 'Khujun/main_login.html')

#Teacher Login
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                if TeacherRegistration.objects.filter(user=user):
                    if TeacherRegistration.objects.filter(user=user, verify='Yes').exists():
                        login(request, user)
                        profiles = TeacherProfile.objects.all()
                        context = {
                            'profiles': profiles,
                        }
                        return render(request, 'Khujun/teacher_dashboard.html', context)
                    elif TeacherRegistration.objects.filter(user=user, verify='').exists():
                        return render(request, 'Khujun/login.html',
                                      {'error_message': 'আপনার একাউন্টটি যাচাই করা হয়নি '})
                    else:
                        return render(request, 'Khujun/login.html', {'error_message': 'Invalid login'})
                else:
                    context = {
                        'guardian': 'guardian',
                    }
                    return render(request, 'Khujun/login.html', context)
            else:
                return render(request, 'Khujun/login.html')
        else:
            return render(request, 'Khujun/login.html', {'error_message': 'Invalid login'})
    else:
        user = request.user
        if user.is_active:
            if TeacherRegistration.objects.filter(user=user):
                context = {
                    'teacher': 'teacher',
                }
            elif GuardianRegistration.objects.filter(user=user):
                context = {
                    'guardian': 'guardian',
                }
            return render(request, 'Khujun/login.html', context)
        else:
            return render(request, 'Khujun/login.html')

#Guardian Login
def login_users(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                if GuardianRegistration.objects.filter(user=user):
                    if GuardianRegistration.objects.filter(user=user, verify='Yes').exists():
                        login(request, user)
                        profiles = TeacherProfile.objects.all()
                        g_profiles = GuardianProfile.objects.all()
                        context = {
                            'profiles': profiles,
                            'g_profiles': g_profiles,
                        }
                        return render(request, 'Khujun/guardian_dashboard.html', context)
                    elif GuardianRegistration.objects.filter(user=user, verify='').exists():
                        return render(request, 'Khujun/logins.html',
                                      {'error_message': 'আপনার একাউন্টটি যাচাই করা হয়নি '})
                    else:
                        return render(request, 'Khujun/logins.html', {'error_message': 'Invalid login'})
                else:
                    context = {
                        'teacher': 'teacher',
                    }
                    return render(request, 'Khujun/logins.html', context)
            else:
                return render(request, 'Khujun/logins.html')
        else:
            return render(request, 'Khujun/logins.html', {'error_message': 'Invalid login'})
    else:
        user = request.user
        if user.is_active:
            if TeacherRegistration.objects.filter(user=user):
                context = {
                    'teacher': 'teacher',
                }
            elif GuardianRegistration.objects.filter(user=user):
                context = {
                    'guardian': 'guardian',
                }
            return render(request, 'Khujun/logins.html', context)
        else:
            return render(request, 'Khujun/logins.html')



#Teacher Registration
def register(request):
    form = UserForm(request.POST or None)
    teacher_reg_form = TeacherRegistrationForm(request.POST or None)
    if form.is_valid() and teacher_reg_form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        user.set_password(password)
        user.save()
        profile = teacher_reg_form.save(commit=False)
        profile.user = user
        profile.save()
        TeacherProfile.objects.create(user=user)
        #user = authenticate(username=username, password=password)
        #if user is not None:
            #if user.is_active:
                #login(request, user)
        TeacherProfile.objects.filter(user=user).update(email=email, username=username)
        messages.info(request, 'আপনার রেজিস্ট্রেশন সম্পন্ন হয়েছে')
        return render(request, 'Khujun/login.html')
    context = {
        "form": form,
        "teacher_reg_form": teacher_reg_form,
    }
    return render(request, 'Khujun/register.html', context)

#Guardian Registration
def registers(request):
    form = UserForm(request.POST or None)
    guardian_reg_form = GuardianRegistrationForm(request.POST or None)
    if form.is_valid() and guardian_reg_form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        user.set_password(password)
        user.save()
        profile = guardian_reg_form.save(commit=False)
        profile.user = user
        profile.save()
        GuardianProfile.objects.create(user=user)
        #user = authenticate(username=username, password=password)
        #if user is not None:
            #if user.is_active:
                #login(request, user)
        GuardianProfile.objects.filter(user=user).update(email=email, username=username)
        messages.info(request, 'আপনার রেজিস্ট্রেশন সম্পন্ন হয়েছে')
        return render(request, 'Khujun/logins.html')
    context = {
        "form": form,
        "guardian_reg_form": guardian_reg_form,
    }
    return render(request, 'Khujun/registers.html', context)


@login_required
def teacher_profile_edit(request):
    user = request.user
    if user.is_active:
        if TeacherRegistration.objects.filter(user=user):
            teacher_profile_edit = TeacherProfileForm(request.POST or None, instance=request.user.teacherprofile)
            if teacher_profile_edit.is_valid():
                profiles = TeacherProfile.objects.filter(user=request.user).get(),
                teacher_profile_edit.save()
                context = {
                    'profiles': profiles,
                    'teacher_profile_edit': teacher_profile_edit,
                }
                messages.info(request, 'আপনার প্রোফাইলটি আপডেট হয়েছে')
                return render(request, 'Khujun/teacher_profile_edit.html', context)

            profiles = TeacherProfile.objects.filter(user=request.user).get(),
            teacher_profile_edit = TeacherProfileForm(instance=request.user.teacherprofile)

            context = {
                'profiles': profiles,
                'teacher_profile_edit': teacher_profile_edit,
            }
            print(context)

            return render(request, 'Khujun/teacher_profile_edit.html', context)
        else:
            context = {
                'guardian': 'guardian',
            }
            return render(request, 'Khujun/main_login.html',context)
    else:
        return render(request, 'Khujun/main_login.html')

@login_required
def teacher_image_edit(request):
    user = request.user
    if user.is_active:
        if TeacherRegistration.objects.filter(user=user):
            if request.method == 'POST':
                teacher_profile_edit = TeacherProfileForm(instance=request.user.teacherprofile)
                uploaded_file = request.FILES['images']
                fs = FileSystemStorage()
                urls = uploaded_file.name
                file_type = urls.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    profiles = TeacherProfile.objects.all()
                    context = {
                        'profiles': profiles,
                    }
                    print(context)
                    messages.info(request, 'আপনার প্রোফাইল ছবিটি অবশ্যই PNG, JPG, or JPEG ফরমেটে থাকতে হবে')
                    return render(request, 'Khujun/teacher_dashboard.html', context)
                else:
                    names = fs.save(uploaded_file.name, uploaded_file)
                    url = fs.url(names)
                    print(uploaded_file.name)
                    print(uploaded_file.size)
                    profile = TeacherProfile.objects.filter(user=request.user).get()
                    profile.images = url
                    profile.save()

                    profiles = TeacherProfile.objects.all()
                    context = {
                        'profiles': profiles,
                    }
                    print(context)
                    messages.info(request, 'আপনার প্রোফাইল ছবিটি আপডেট হয়েছে')
                    return render(request, 'Khujun/teacher_dashboard.html', context)
            else:
                profiles = TeacherProfile.objects.filter(user=request.user).get(),
                teacher_profile_edit = TeacherProfileForm(instance=request.user.teacherprofile)

                context = {
                    'profiles': profiles,
                    'teacher_profile_edit': teacher_profile_edit,
                }
                return render(request, 'Khujun/teacher_profile_edit.html', context)
        else:
            context = {
                'guardian': 'guardian',
            }
            return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/main_login.html')


@login_required
def guardian_profile_edit(request):
    user = request.user
    if user.is_active:
        if GuardianRegistration.objects.filter(user=user):
            guardian_profile_edit = GuardianProfileForm(request.POST or None, instance=request.user.guardianprofile)
            if guardian_profile_edit.is_valid():
                profiles = GuardianProfile.objects.filter(user=request.user).get(),
                guardian_profile_edit.save()
                context = {
                    'profiles': profiles,
                    'guardian_profile_edit': guardian_profile_edit,
                }
                messages.info(request, 'আপনার প্রোফাইলটি আপডেট হয়েছে')
                return render(request, 'Khujun/guardian_profile_edit.html', context)

            profiles = GuardianProfile.objects.filter(user=request.user).get(),
            guardian_profile_edit = GuardianProfileForm(instance=request.user.guardianprofile)

            context = {
                'profiles': profiles,
                'guardian_profile_edit': guardian_profile_edit,
            }
            print(context)
            return render(request, 'Khujun/guardian_profile_edit.html', context)
        else:
            context = {
                'teacher': 'teacher',
            }
            return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/main_login.html')

@login_required
def guardian_image_edit(request):
    user = request.user
    if user.is_active:
        if GuardianRegistration.objects.filter(user=user):
            if request.method == 'POST':
                guardian_profile_edit = GuardianProfileForm(instance=request.user.guardianprofile)
                uploaded_file = request.FILES['images']
                fs = FileSystemStorage()
                urls = uploaded_file.name
                file_type = urls.split('.')[-1]
                file_type = file_type.lower()
                if file_type not in IMAGE_FILE_TYPES:
                    profiles = TeacherProfile.objects.all()
                    g_profiles = GuardianProfile.objects.all()
                    context = {
                        'profiles': profiles,
                        'g_profiles': g_profiles,
                    }
                    print(context)
                    messages.info(request, 'আপনার প্রোফাইল ছবিটি অবশ্যই PNG, JPG, or JPEG ফরমেটে থাকতে হবে')
                    return render(request, 'Khujun/guardian_dashboard.html', context)
                else:
                    names = fs.save(uploaded_file.name, uploaded_file)
                    url = fs.url(names)
                    print(uploaded_file.name)
                    print(uploaded_file.size)
                    profile = GuardianProfile.objects.filter(user=request.user).get()
                    profile.images = url
                    profile.save()

                    profiles = TeacherProfile.objects.all()
                    g_profiles = GuardianProfile.objects.all()
                    context = {
                        'profiles': profiles,
                        'g_profiles': g_profiles,
                    }
                    print(context)
                    messages.info(request, 'আপনার প্রোফাইল ছবিটি আপডেট হয়েছে')
                    return render(request, 'Khujun/guardian_dashboard.html', context)
            else:
                profiles = GuardianProfile.objects.filter(user=request.user).get(),
                guardian_profile_edit = GuardianProfileForm(instance=request.user.guardianprofile)

                context = {
                    'profiles': profiles,
                    'guardian_profile_edit': guardian_profile_edit,
                }
                return render(request, 'Khujun/guardian_profile_edit.html', context)
        else:
            context = {
                'teacher': 'teacher',
            }
            return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/main_login.html')

@login_required
def teacher_dashboard(request):
    user = request.user
    if user.is_active:
        if TeacherRegistration.objects.filter(user=user):
            profiles = TeacherProfile.objects.all()
            context = {
                'profiles': profiles,
            }
            return render(request, 'Khujun/teacher_dashboard.html', context)
        else:
            context = {
                'guardian': 'guardian',
            }
            return render(request, 'Khujun/main_login.html',context)
    else:
        return render(request, 'Khujun/main_login.html')


def teachersprofile(request, id):
    user = request.user
    if user.is_active:
        if TeacherRegistration.objects.filter(user=user):
            profile = get_object_or_404(TeacherProfile, pk=id)
            username = profile.username
            if not TeacherRating.objects.filter(teacher_username=username):
                behaviour_rating = 0
                teaching_rating = 0
                response_rating = 0
                bio_rating = 0
            else:
                behaviour_ratings = TeacherRating.objects.filter(teacher_username=username).aggregate(
                    Avg('behaviour_rating'))
                behaviour_rating = round(behaviour_ratings['behaviour_rating__avg'])
                print(behaviour_ratings)
                print(behaviour_rating)
                teaching_ratings = TeacherRating.objects.filter(teacher_username=username).aggregate(
                    Avg('teaching_rating'))
                teaching_rating = round(teaching_ratings['teaching_rating__avg'])
                response_ratings = TeacherRating.objects.filter(teacher_username=username).aggregate(
                    Avg('response_rating'))
                response_rating = round(response_ratings['response_rating__avg'])
                bio_ratings = TeacherRating.objects.filter(teacher_username=username).aggregate(Avg('bio_rating'))
                bio_rating = round(bio_ratings['bio_rating__avg'])

            profiles = TeacherProfile.objects.all()

            return render(request, 'Khujun/teachers_profile_details.html',
                          {'profile': profile, 'user': user, 'behaviour_rating': behaviour_rating,
                           'teaching_rating': teaching_rating, 'response_rating': response_rating,
                           'bio_rating': bio_rating,'profiles':profiles})
        else:
            context = {
                'guardian': 'guardian',
            }
            return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/main_login.html')


@login_required
def guardian_dashboard(request):
    user = request.user
    if user.is_active:
        if GuardianRegistration.objects.filter(user=user):
            profiles = TeacherProfile.objects.all()
            g_profiles = GuardianProfile.objects.all()
            context = {
                'profiles': profiles,
                'g_profiles': g_profiles,
            }
            return render(request, 'Khujun/guardian_dashboard.html', context)
        else:
            context = {
                'teacher': 'teacher',
            }
            return render(request, 'Khujun/main_login.html',context)
    else:
        return render(request, 'Khujun/main_login.html')

def teacherprofile(request, id):
        user = request.user
        if user.is_active:
            if GuardianRegistration.objects.filter(user=user):
                profile = get_object_or_404(TeacherProfile, pk=id)
                username = profile.username
                if not TeacherRating.objects.filter(teacher_username=username):
                    behaviour_rating = 0
                    teaching_rating = 0
                    response_rating = 0
                    bio_rating = 0

                else:
                    behaviour_ratings = TeacherRating.objects.filter(teacher_username=username).aggregate(
                        Avg('behaviour_rating'))
                    behaviour_rating = round(behaviour_ratings['behaviour_rating__avg'])
                    # print(behaviour_ratings)
                    # print(behaviour_rating)
                    teaching_ratings = TeacherRating.objects.filter(teacher_username=username).aggregate(
                        Avg('teaching_rating'))
                    teaching_rating = round(teaching_ratings['teaching_rating__avg'])
                    response_ratings = TeacherRating.objects.filter(teacher_username=username).aggregate(
                        Avg('response_rating'))
                    response_rating = round(response_ratings['response_rating__avg'])
                    bio_ratings = TeacherRating.objects.filter(teacher_username=username).aggregate(Avg('bio_rating'))
                    bio_rating = round(bio_ratings['bio_rating__avg'])

                profiles = GuardianProfile.objects.all()

                return render(request, 'Khujun/teacher_profile_details.html',
                              {'profile': profile, 'user': user, 'behaviour_rating': behaviour_rating,
                               'teaching_rating': teaching_rating, 'response_rating': response_rating,
                               'bio_rating': bio_rating,'profiles':profiles})
            else:
                context = {
                    'teacher': 'teacher',
                }
                return render(request, 'Khujun/main_login.html', context)
        else:
            return render(request, 'Khujun/main_login.html')

@login_required
def teacherrating(request,id):
        user = request.user
        if user.is_active:
            if GuardianRegistration.objects.filter(user=user):
                teacher_profile = TeacherProfile.objects.filter(pk=id).get()
                teacher_name = teacher_profile.user.username
                if not TeacherRating.objects.filter(user=user, teacher_username=teacher_name):
                    TeacherRating.objects.create(user=user, teacher_username=teacher_name)
                else:
                    teacher_rating = TeacherRating.objects.get(user=user, teacher_username=teacher_name)
                    teacherrating = TeacherRatingForm(request.POST or None, instance=teacher_rating)
                    if teacherrating.is_valid():
                        # profiles = GuardianProfile.objects.filter(user=request.user).get(),
                        teacherrating.save()
                        teacher_profile = TeacherProfile.objects.filter(pk=id).get()
                        teacher_name = teacher_profile.user.username
                        teacher_firstname = teacher_profile.first_name
                        teacher_lastname = teacher_profile.last_name
                        TeacherRating.objects.filter(user=user, teacher_username=teacher_name).update(
                            teacher_username=teacher_name,
                            teacher_firstname=teacher_firstname,
                            teacher_lastname=teacher_lastname)

                        g_profiles = GuardianProfile.objects.all()
                        context = {
                            'teacherrating': teacherrating,
                            'g_profiles': g_profiles,
                        }
                        messages.info(request, 'আপনার রেটিং প্রদান সম্পন্ন হয়েছে')
                        return render(request, 'Khujun/teacherrating.html', context)
                # profiles = GuardianProfile.objects.filter(user=request.user).get(),
                teacher_rating = TeacherRating.objects.get(user=user, teacher_username=teacher_name)
                teacherrating = TeacherRatingForm(instance=teacher_rating)

                g_profiles = GuardianProfile.objects.all()
                context = {
                    'teacherrating': teacherrating,
                    'g_profiles': g_profiles,
                }
                print(context)
                return render(request, 'Khujun/teacherrating.html', context)
            else:
                context = {
                    'teacher': 'teacher',
                }
                return render(request, 'Khujun/main_login.html', context)
        else:
            return render(request, 'Khujun/main_login.html')

def teacherrequests(request, id):
    user = request.user
    if user.is_active:
        if GuardianRegistration.objects.filter(user=user):
            teacherrequest = TuitionInfoForm(request.POST or None)
            if teacherrequest.is_valid():
                user = request.user
                profile = teacherrequest.save(commit=False)
                profile.user = user
                profile.save()
                teacher_profile = TeacherProfile.objects.filter(pk=id).get()
                teacher_name = teacher_profile.user.username
                teacher_email = teacher_profile.email
                teacher_firstname = teacher_profile.first_name
                teacher_lastname = teacher_profile.last_name
                tuition_id_info = TuitionInfo.objects.filter(user=user).latest('id')
                tuition_id = tuition_id_info.pk
                TuitionInfo.objects.filter(user=user, pk=tuition_id).update(teacher_username=teacher_name,
                                                                            teacher_firstname=teacher_firstname,
                                                                            teacher_lastname=teacher_lastname)
                #TeacherProfile.objects.filter(username=teacher_name).update(notification='1')
                # profile = TeacherProfile.objects.filter(user=user).get()
                count = teacher_profile.notifications
                count1 = teacher_profile.notification
                count = count + 1
                count1 = count1 + 1
                teacher_profile.notification = count1
                teacher_profile.notifications = count
                teacher_profile.save()
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        # info = TuitionInfo.objects.latest('id',user=user)
                        # info = get_object_or_404(TuitionInfo, user=user)
                        info = TuitionInfo.objects.filter(user=user).latest('id')
                        classes = info.classes
                        subject = info.subject
                        day = info.day
                        payment = info.payment
                        institute_name = info.institute_name
                        address = info.address

                        email_user = 'tuition.info.bd@gmail.com'
                        email_password = 'Tuitioninfo2019'
                        email_send = teacher_email

                        subjects = 'টিউশনের অনুরোধ'

                        msg = MIMEMultipart()
                        msg['From'] = email_user
                        msg['To'] = email_send
                        msg['Subject'] = subjects

                        body = "শ্রেণীঃ " + classes + "\nবিষয়ঃ " + subject + "\nসাপ্তাহিক দিনঃ " + day + "\nপ্রদত্ত অর্থঃ " + payment + "\nবিদ্যালয়/কলেজের নামঃ " + institute_name + "\nঠিকানাঃ " + address
                        msg.attach(MIMEText(body, 'plain'))
                        text = msg.as_string()
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(email_user, email_password)

                        server.sendmail(email_user, email_send, text)
                        server.quit()

                        profiles = TeacherProfile.objects.all()
                        g_profiles = GuardianProfile.objects.all()
                        context = {
                            'g_profiles': g_profiles,
                            'profiles': profiles,
                        }
                        messages.info(request,'আপনার অনুরোধটি পাঠানো হয়েছে')
                        return render(request, 'Khujun/guardian_dashboard.html',context)

            g_profiles = GuardianProfile.objects.all()
            context = {
                "teacherrequest": teacherrequest,
                'g_profiles': g_profiles,
            }
            return render(request, 'Khujun/teacherrequests.html', context)
        else:
            context = {
                'teacher': 'teacher',
            }
            return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/main_login.html')

def details_tuition_info(request, id):
    user = request.user
    if user.is_active:
        if TeacherRegistration.objects.filter(user=user):
            login(request, user)
            t_profiles = TeacherProfile.objects.all()
            profile = TuitionInfo.objects.filter(pk=id).get()
            teacher_confirm = profile.teacher_confirm
            guardian_confirm = profile.guardian_confirm
            if (teacher_confirm == 1 and guardian_confirm == 1):
                messages.info(request,
                              'আপনি এবং সংশ্লিষ্ট অভিভাবক উভয়ই ইতোমধ্যে টিউশনটি নিশ্চিত করেছেন।সরাসরি যোগাযোগ করুনঃ ০১৯২৫৪৪৪৭৭৭')
                return render(request, 'Khujun/details_tuition_info.html', {'profile': profile, 'user': user,'t_profiles': t_profiles})
            elif (teacher_confirm == 1 and guardian_confirm == 0):
                messages.info(request,
                              'আপনি ইতোমধ্যে টিউশনটি গ্রহণ করেছেন।সংশ্লিষ্ট অভিভাবকের নিশ্চিতকরণের জন্য অপেক্ষা করুন')
                return render(request, 'Khujun/details_tuition_info.html',{'profile': profile, 'user': user,'t_profiles': t_profiles})
            elif (teacher_confirm == 1 and guardian_confirm == 2):
                messages.info(request, 'সংশ্লিষ্ট অভিভাবক ইতোমধ্যে টিউশনটি বর্জন করেছেন।')
                return render(request, 'Khujun/details_tuition_info.html', {'profile': profile, 'user': user,'t_profiles': t_profiles})
            elif (teacher_confirm == 2):
                messages.info(request, 'আপনি ইতোমধ্যে টিউশনটি বর্জন করেছেন।')
                return render(request, 'Khujun/details_tuition_info.html', {'profile': profile, 'user': user,'t_profiles': t_profiles})
            else:
                return render(request, 'Khujun/details_tuition_info.html', {'profile': profile, 'user': user,'t_profiles': t_profiles})
        else:
            context = {
                'guardian': 'guardian',
            }
            return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/main_login.html')

def teacher_accept(request, id):
    user = request.user
    if user.is_active:
        if TeacherRegistration.objects.filter(user=user):
            login(request, user)
            tuition_info = TuitionInfo.objects.filter(pk=id).get()
            g_username = tuition_info.user
            profile = GuardianProfile.objects.filter(user=g_username).get()
            count = profile.notifications
            count1 = profile.notification
            count = count + 1
            count1 = count1 + 1
            profile.notification = count1
            profile.notifications = count
            profile.save()

            g_email = profile.email

            teacher_info = TeacherProfile.objects.filter(user=user).get()
            first_names = teacher_info.first_name
            last_names = teacher_info.last_name
            full_name = first_names + " " + last_names

            classes = tuition_info.classes
            subject = tuition_info.subject
            day = tuition_info.day
            payment = tuition_info.payment
            institute_name = tuition_info.institute_name
            address = tuition_info.address

            email_user = 'tuition.info.bd@gmail.com'
            email_password = 'Tuitioninfo2019'
            email_send = g_email

            subjects = 'টিউশনের অনুরোধ'

            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_send
            msg['Subject'] = subjects

            body = "শ্রেণীঃ " + classes + "\nবিষয়ঃ " + subject + "\nসাপ্তাহিক দিনঃ " + day + "\nপ্রদত্ত অর্থঃ " + payment + "\nবিদ্যালয়/কলেজের নামঃ " + institute_name + "\nঠিকানাঃ " + address + "\nজনাব " + full_name + " আপনার উপরোক্ত টিউশনের অনুরোধটি গ্রহণ করেছেন"
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)

            server.sendmail(email_user, email_send, text)
            server.quit()

            tuition_info.teacher_confirm = 1
            tuition_info.save()

            t_profiles = TeacherProfile.objects.all()
            profile = TuitionInfo.objects.filter(pk=id).get()
            messages.info(request, 'আপনি টিউশনটি গ্রহণ করেছেন')
            return render(request, 'Khujun/details_tuition_info.html', {'profile': profile, 'user': user,'t_profiles': t_profiles})
        else:
            context = {
                'guardian': 'guardian',
            }
            return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/main_login.html')

def teacher_reject(request, id):
    user = request.user
    if user.is_active:
        if TeacherRegistration.objects.filter(user=user):
            login(request, user)
            tuition_info = TuitionInfo.objects.filter(pk=id).get()
            g_username = tuition_info.user
            profile = GuardianProfile.objects.filter(user=g_username).get()
            count = profile.notifications
            count1 = profile.notification
            count = count + 1
            count1 = count1 + 1
            profile.notification = count1
            profile.notifications = count
            profile.save()

            g_email = profile.email

            teacher_info = TeacherProfile.objects.filter(user=user).get()
            first_names = teacher_info.first_name
            last_names = teacher_info.last_name
            full_name = first_names + " " + last_names

            classes = tuition_info.classes
            subject = tuition_info.subject
            day = tuition_info.day
            payment = tuition_info.payment
            institute_name = tuition_info.institute_name
            address = tuition_info.address

            email_user = 'tuition.info.bd@gmail.com'
            email_password = 'Tuitioninfo2019'
            email_send = g_email

            subjects = 'টিউশনের অনুরোধ'

            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_send
            msg['Subject'] = subjects

            body = "শ্রেণীঃ " + classes + "\nবিষয়ঃ " + subject + "\nসাপ্তাহিক দিনঃ " + day + "\nপ্রদত্ত অর্থঃ " + payment + "\nবিদ্যালয়/কলেজের নামঃ " + institute_name + "\nঠিকানাঃ " + address + "\nদুঃখিত, জনাব " + full_name + " আপনার উপরোক্ত টিউশনের অনুরোধটি এই মুহূর্তে গ্রহণ করতে পারছেন না।"
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)

            server.sendmail(email_user, email_send, text)
            server.quit()

            tuition_info.teacher_confirm = 2
            tuition_info.save()

            t_profiles = TeacherProfile.objects.all()

            profile = TuitionInfo.objects.filter(pk=id).get()
            messages.info(request, 'আপনি টিউশনটি বর্জন করেছেন')
            return render(request, 'Khujun/details_tuition_info.html', {'profile': profile, 'user': user,'t_profiles': t_profiles})
        else:
            context = {
                'guardian': 'guardian',
            }
            return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/main_login.html')

def details_tuitions_info(request, id):
    user = request.user
    if user.is_active:
        if GuardianRegistration.objects.filter(user=user):
            login(request, user)
            g_profiles = GuardianProfile.objects.all()
            context = {

                'g_profiles': g_profiles,
            }
            profile = TuitionInfo.objects.filter(pk=id).get()
            teacher_confirm = profile.teacher_confirm
            guardian_confirm = profile.guardian_confirm
            if (teacher_confirm == 1 and guardian_confirm == 1):
                messages.info(request,
                              'আপনি এবং সংশ্লিষ্ট শিক্ষক/শিক্ষিকা উভয়ই ইতোমধ্যে টিউশনটি নিশ্চিত করেছেন।সরাসরি যোগাযোগ করুনঃ ০১৯২৫৪৪৪৭৭৭')
                return render(request, 'Khujun/details_tuitions_info.html', {'profile': profile, 'user': user,'g_profiles': g_profiles})
            elif (teacher_confirm == 0 and guardian_confirm == 0):
                messages.info(request,
                              'সংশ্লিষ্ট শিক্ষক/শিক্ষিকা এখনও পর্যন্ত আপনার উক্ত টিউশনটি গ্রহণ/বর্জন করেননি। অনুগ্রহ পূর্বক অপেক্ষা করুন')
                return render(request, 'Khujun/details_tuitions_info.html', {'profile': profile, 'user': user,'g_profiles': g_profiles})
            elif (teacher_confirm == 2 and guardian_confirm == 0):
                messages.info(request, 'সংশ্লিষ্ট শিক্ষক/শিক্ষিকা ইতোমধ্যে টিউশনটি বর্জন করেছেন।')
                return render(request, 'Khujun/details_tuitions_info.html', {'profile': profile, 'user': user,'g_profiles': g_profiles})
            elif (guardian_confirm == 2):
                messages.info(request, 'আপনি ইতোমধ্যে টিউশনটি বর্জন করেছেন।')
                return render(request, 'Khujun/details_tuitions_info.html', {'profile': profile, 'user': user,'g_profiles': g_profiles})
            else:
                return render(request, 'Khujun/details_tuitions_info.html', {'profile': profile, 'user': user,'g_profiles': g_profiles})
        else:
            context = {
                'teacher': 'teacher',
            }
            return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/main_login.html')

def guardian_accept(request, id):
    user = request.user
    if user.is_active:
        if GuardianRegistration.objects.filter(user=user):
            login(request, user)
            tuition_info = TuitionInfo.objects.filter(pk=id).get()
            t_username = tuition_info.teacher_username
            profile = TeacherProfile.objects.filter(username=t_username).get()
            count = profile.notifications
            count1 = profile.notification
            count = count + 1
            count1 = count1 + 1
            profile.notification = count1
            profile.notifications = count
            profile.save()

            t_email = profile.email

            guardian_profile = GuardianProfile.objects.filter(user=user).get()
            g_email = guardian_profile.email

            first_names = tuition_info.teacher_firstname
            last_names = tuition_info.teacher_lastname
            full_name = first_names + " " + last_names

            classes = tuition_info.classes
            subject = tuition_info.subject
            day = tuition_info.day
            payment = tuition_info.payment
            institute_name = tuition_info.institute_name
            address = tuition_info.address

            email_user = 'tuition.info.bd@gmail.com'
            email_password = 'Tuitioninfo2019'
            email_send = g_email
            email_sends = t_email

            subjects = 'টিউশনের অনুরোধ'

            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_send
            msg['Subject'] = subjects

            body = "শ্রেণীঃ " + classes + "\nবিষয়ঃ " + subject + "\nসাপ্তাহিক দিনঃ " + day + "\nপ্রদত্ত অর্থঃ " + payment + "\nবিদ্যালয়/কলেজের নামঃ " + institute_name + "\nঠিকানাঃ " + address + "\nধন্যবাদ।\nআপনি জনাব " + full_name + " এর উপরোক্ত টিউশনের অনুরোধটি নিশ্চিত করেছেন।\n\nসরাসরি যোগাযোগ করুনঃ ০১৯২৫৪৪৪৭৭৭\n"
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)

            server.sendmail(email_user, email_send, text)
            server.quit()

            msgs = MIMEMultipart()
            msgs['From'] = email_user
            msgs['To'] = email_sends
            msgs['Subject'] = subjects

            bodys = "শ্রেণীঃ " + classes + "\nবিষয়ঃ " + subject + "\nসাপ্তাহিক দিনঃ " + day + "\nপ্রদত্ত অর্থঃ " + payment + "\nবিদ্যালয়/কলেজের নামঃ " + institute_name + "\nঠিকানাঃ " + address + "\nআপনার উপরোক্ত টিউশনের অনুরোধটি কাঙ্ক্ষিত অভিভাবক গ্রহণ করেছেন।\n\nসরাসরি যোগাযোগ করুনঃ ০১৯২৫৪৪৪৭৭৭\n"
            msgs.attach(MIMEText(bodys, 'plain'))
            texts = msgs.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)

            server.sendmail(email_user, email_sends, texts)
            server.quit()

            tuition_info.guardian_confirm = 1
            tuition_info.save()

            g_profiles = GuardianProfile.objects.all()
            profile = TuitionInfo.objects.filter(pk=id).get()
            messages.info(request, 'আপনি টিউশনটি গ্রহণ করেছেন')
            return render(request, 'Khujun/details_tuitions_info.html',{'profile': profile, 'user': user,'g_profiles': g_profiles})
        else:
            context = {
                'teacher': 'teacher',
            }
            return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/main_login.html')

def guardian_reject(request, id):
    user = request.user
    if user.is_active:
        if GuardianRegistration.objects.filter(user=user):
            login(request, user)
            tuition_info = TuitionInfo.objects.filter(pk=id).get()
            t_username = tuition_info.teacher_username
            profile = TeacherProfile.objects.filter(username=t_username).get()
            count = profile.notifications
            count1 = profile.notification
            count = count + 1
            count1 = count1 + 1
            profile.notification = count1
            profile.notifications = count
            profile.save()

            t_email = profile.email

            guardian_profile = GuardianProfile.objects.filter(user=user).get()
            g_email = guardian_profile.email

            first_names = tuition_info.teacher_firstname
            last_names = tuition_info.teacher_lastname
            full_name = first_names + " " + last_names

            classes = tuition_info.classes
            subject = tuition_info.subject
            day = tuition_info.day
            payment = tuition_info.payment
            institute_name = tuition_info.institute_name
            address = tuition_info.address

            email_user = 'tuition.info.bd@gmail.com'
            email_password = 'Tuitioninfo2019'
            email_send = g_email
            email_sends = t_email

            subjects = 'টিউশনের অনুরোধ'

            msg = MIMEMultipart()
            msg['From'] = email_user
            msg['To'] = email_send
            msg['Subject'] = subjects

            body = "শ্রেণীঃ " + classes + "\nবিষয়ঃ " + subject + "\nসাপ্তাহিক দিনঃ " + day + "\nপ্রদত্ত অর্থঃ " + payment + "\nবিদ্যালয়/কলেজের নামঃ " + institute_name + "\nঠিকানাঃ " + address + "\nধন্যবাদ।\nআপনি জনাব " + full_name + " এর উপরোক্ত টিউশনের অনুরোধটি বর্জন করেছেন।\n"
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)

            server.sendmail(email_user, email_send, text)
            server.quit()

            msgs = MIMEMultipart()
            msgs['From'] = email_user
            msgs['To'] = email_sends
            msgs['Subject'] = subjects

            bodys = "শ্রেণীঃ " + classes + "\nবিষয়ঃ " + subject + "\nসাপ্তাহিক দিনঃ " + day + "\nপ্রদত্ত অর্থঃ " + payment + "\nবিদ্যালয়/কলেজের নামঃ " + institute_name + "\nঠিকানাঃ " + address + "\nদুঃখিত,\nআপনার উপরোক্ত টিউশনের অনুরোধটি কাঙ্ক্ষিত অভিভাবক গ্রহণ করেনি\n"
            msgs.attach(MIMEText(bodys, 'plain'))
            texts = msgs.as_string()
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email_user, email_password)

            server.sendmail(email_user, email_sends, texts)
            server.quit()

            tuition_info.guardian_confirm = 2
            tuition_info.save()

            g_profiles = GuardianProfile.objects.all()
            profile = TuitionInfo.objects.filter(pk=id).get()
            messages.info(request, 'আপনি টিউশনটি বর্জন করেছেন')
            return render(request, 'Khujun/details_tuitions_info.html',{'profile': profile, 'user': user,'g_profiles': g_profiles})
        else:
            context = {
                'teacher': 'teacher',
            }
            return render(request, 'Khujun/main_login.html', context)
    else:
        return render(request, 'Khujun/main_login.html')

def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'Khujun/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'Khujun/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })

'''def handler404(request, exception):
    return render(request, 'errors/404.html', locals())'''