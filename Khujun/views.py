from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .forms import AlbumForm, SongForm, UserForm, TeacherRegistrationForm , GuardianRegistrationForm, TeacherProfileForm, GuardianProfileForm
from .models import TeacherRegistration,GuardianRegistration
from .models import Album, Song, TeacherProfile, GuardianProfile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

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


def mainreg(request):
    return render(request, 'Khujun/main_register.html')

def mainlogin(request):
    return render(request, 'Khujun/main_login.html')

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'Khujun/login.html', context)

#Teacher Login
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if TeacherRegistration.objects.filter(user=request.user,verify='Yes').exists():
                    albums = Album.objects.filter(user=request.user)
                    return render(request, 'Khujun/index.html', {'albums': albums})
                else:
                    return render(request, 'Khujun/login.html', {'error_message': 'আপনার একাউন্টটি যাচাই করা হয়নি '})
            else:
                return render(request, 'Khujun/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'Khujun/login.html', {'error_message': 'Invalid login'})
    return render(request, 'Khujun/login.html')

#Guardian Login
def login_users(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                if GuardianRegistration.objects.filter(user=request.user,verify='Yes').exists():
                    albums = Album.objects.filter(user=request.user)
                    return render(request, 'Khujun/indexs.html', {'albums': albums})
                else:
                    return render(request, 'Khujun/logins.html', {'error_message': 'আপনার একাউন্টটি যাচাই করা হয়নি '})
            else:
                return render(request, 'Khujun/logins.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'Khujun/logins.html', {'error_message': 'Invalid login'})
    return render(request, 'Khujun/logins.html')


#Teacher Registration
def register(request):
    form = UserForm(request.POST or None)
    teacher_reg_form = TeacherRegistrationForm(request.POST or None)
    if form.is_valid() and teacher_reg_form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        profile = teacher_reg_form.save(commit=False)
        profile.user = user
        profile.save()
        TeacherProfile.objects.create(user=user)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
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
        user.set_password(password)
        user.save()
        profile = guardian_reg_form.save(commit=False)
        profile.user = user
        profile.save()
        GuardianProfile.objects.create(user=user)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.info(request, 'আপনার রেজিস্ট্রেশন সম্পন্ন হয়েছে')
                return render(request, 'Khujun/login.html')
    context = {
        "form": form,
        "guardian_reg_form": guardian_reg_form,
    }
    return render(request, 'Khujun/registers.html', context)


@login_required
def teacher_profile_edit(request):
        teacher_profile_edit = TeacherProfileForm(request.POST or None,instance=request.user.teacherprofile)
        if teacher_profile_edit.is_valid():
            profiles = TeacherProfile.objects.filter(user=request.user).get(),
            teacher_profile_edit.save()
            context = {
                'profiles': profiles,
                'teacher_profile_edit': teacher_profile_edit,
            }
            messages.info(request, 'আপনার প্রোফাইলটি আপডেট হয়েছে')
            return render(request, 'Khujun/teacher_profile_edit.html',context)

        profiles = TeacherProfile.objects.filter(user=request.user).get(),
        teacher_profile_edit = TeacherProfileForm(instance=request.user.teacherprofile)

        context = {
            'profiles': profiles,
            'teacher_profile_edit': teacher_profile_edit,
        }
        print(context)
        return render(request, 'Khujun/teacher_profile_edit.html', context)

@login_required
def teacher_image_edit(request):
    if request.method == 'POST':
        teacher_profile_edit = TeacherProfileForm(instance=request.user.teacherprofile)
        uploaded_file = request.FILES['images']
        fs = FileSystemStorage()
        names = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(names)
        print(uploaded_file.name)
        print(uploaded_file.size)
        profile = TeacherProfile.objects.filter(user=request.user).get()
        profile.images = url
        profile.save()

        profiles = TeacherProfile.objects.filter(user=request.user).get()
        context = {
            'profiles':profiles,
            'teacher_profile_edit': teacher_profile_edit,
        }
        print(context)
        messages.info(request, 'আপনার প্রোফাইল ছবিটি আপডেট হয়েছে')
        return render(request, 'Khujun/index.html',context)
    else:
        profiles = TeacherProfile.objects.filter(user=request.user).get(),
        teacher_profile_edit = TeacherProfileForm(instance=request.user.teacherprofile)

        context = {
        'profiles': profiles,
        'teacher_profile_edit': teacher_profile_edit,
        }
        return render(request, 'Khujun/teacher_profile_edit.html', context)


@login_required
def guardian_profile_edit(request):
        guardian_profile_edit = GuardianProfileForm(request.POST or None,instance=request.user.guardianprofile)
        if guardian_profile_edit.is_valid():
            profiles = GuardianProfile.objects.filter(user=request.user).get(),
            guardian_profile_edit.save()
            context = {
                'profiles': profiles,
                'guardian_profile_edit': guardian_profile_edit,
            }
            messages.info(request, 'আপনার প্রোফাইলটি আপডেট হয়েছে')
            return render(request, 'Khujun/guardian_profile_edit.html',context)

        profiles = GuardianProfile.objects.filter(user=request.user).get(),
        guardian_profile_edit = GuardianProfileForm(instance=request.user.guardianprofile)

        context = {
            'profiles': profiles,
            'guardian_profile_edit': guardian_profile_edit,
        }
        print(context)
        return render(request, 'Khujun/guardian_profile_edit.html', context)

@login_required
def guardian_image_edit(request):
    if request.method == 'POST':
        guardian_profile_edit = GuardianProfileForm(instance=request.user.guardianprofile)
        uploaded_file = request.FILES['images']
        fs = FileSystemStorage()
        names = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(names)
        print(uploaded_file.name)
        print(uploaded_file.size)
        profile = GuardianProfile.objects.filter(user=request.user).get()
        profile.images = url
        profile.save()

        profiles = GuardianProfile.objects.filter(user=request.user).get()
        context = {
            'profiles':profiles,
            'guardian_profile_edit': guardian_profile_edit,
        }
        print(context)
        messages.info(request, 'আপনার প্রোফাইল ছবিটি আপডেট হয়েছে')
        return render(request, 'Khujun/indexs.html',context)
    else:
        profiles = GuardianProfile.objects.filter(user=request.user).get(),
        guardian_profile_edit = GuardianProfileForm(instance=request.user.guardianprofile)

        context = {
        'profiles': profiles,
        'guardian_profile_edit': guardian_profile_edit,
        }
        return render(request, 'Khujun/guardian_profile_edit.html', context)




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
