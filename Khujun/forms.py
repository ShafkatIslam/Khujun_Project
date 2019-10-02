from django import forms
from django.contrib.auth.models import User
from Khujun.models import TeacherRegistration,GuardianRegistration

from .models import Album, Song


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_title', 'genre', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_title', 'audio_file']


class UserForm(forms.ModelForm):
    username = forms.CharField(label='ব্যবহারকারীর নাম',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='পাসওয়ার্ড',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='ই-মেইল', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        data = self.cleaned_data['email']
        duplicate_users = User.objects.filter(email=data)
        if self.instance.pk is not None:  # If you're editing an user, remove him from the duplicated results
            duplicate_users = duplicate_users.exclude(pk=self.instance.pk)
        if duplicate_users.exists():
            raise forms.ValidationError("ই-মেইলটি ইতোমধ্যে রেজিস্টার্ড")
        return data

BOARDS= [
    ('dhaka', 'Dhaka'),
    ('chittagong', 'Chittagong'),
    ('comilla', 'Comilla'),
    ('rajshahi', 'Rajshahi'),
    ('khulna', 'Khulna'),
    ('sylhet', 'Sylhet'),
    ('dinajpur', 'Dinajpur'),
    ('jessore', 'Jessore'),
    ]

class TeacherRegistrationForm(forms.ModelForm):
    ssc_board = forms.CharField(label='এস.এস.সি বোর্ড:', widget=forms.Select(choices=BOARDS,attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='নামের প্রথম অংশ:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='নামের শেষ অংশ:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.IntegerField(label='মোবাইল নম্বর:', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ssc_roll = forms.IntegerField(label='এস.এস.সি রোল নম্বর:', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    ssc_reg = forms.IntegerField(label='এস.এস.সি রেজিস্ট্রেশন নম্বর:',widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta():
        model = TeacherRegistration
        fields = ('first_name', 'last_name', 'phone_number', 'ssc_roll', 'ssc_reg', 'ssc_board')

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        duplicate_phone_number = TeacherRegistration.objects.filter(phone_number=data)
        if self.instance.pk is not None:  # If you're editing an user, remove him from the duplicated results
            duplicate_phone_number = duplicate_phone_number.exclude(pk=self.instance.pk)
        if duplicate_phone_number.exists():
            raise forms.ValidationError("মোবাইল নম্বরটি ইতোমধ্যে রেজিস্টার্ড")
        return data


    def clean_ssc_roll(self):
        data = self.cleaned_data['ssc_roll']
        duplicate_ssc_roll = TeacherRegistration.objects.filter(ssc_roll=data)
        if self.instance.pk is not None:  # If you're editing an user, remove him from the duplicated results
            duplicate_ssc_roll = duplicate_ssc_roll.exclude(pk=self.instance.pk)
        if duplicate_ssc_roll.exists():
            raise forms.ValidationError("এস.এস.সি রোল নম্বরটি ইতোমধ্যে রেজিস্টার্ড")
        return data

    def clean_ssc_reg(self):
        data = self.cleaned_data['ssc_reg']
        duplicate_ssc_reg = TeacherRegistration.objects.filter(ssc_reg=data)
        if self.instance.pk is not None:  # If you're editing an user, remove him from the duplicated results
            duplicate_ssc_reg = duplicate_ssc_reg.exclude(pk=self.instance.pk)
        if duplicate_ssc_reg.exists():
            raise forms.ValidationError("এস.এস.সি রেজিস্ট্রেশন নম্বরটি ইতোমধ্যে রেজিস্টার্ড")
        return data


class GuardianRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label='নামের প্রথম অংশ:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='নামের শেষ অংশ:', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.IntegerField(label='মোবাইল নম্বর:', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    nid = forms.CharField(label='জাতীয় পরিচয়পত্র নম্বর:', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta():
        model = GuardianRegistration
        fields = ('first_name', 'last_name', 'phone_number', 'nid')

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']
        duplicate_phone_number = GuardianRegistration.objects.filter(phone_number=data)
        if self.instance.pk is not None:  # If you're editing an user, remove him from the duplicated results
            duplicate_phone_number = duplicate_phone_number.exclude(pk=self.instance.pk)
        if duplicate_phone_number.exists():
            raise forms.ValidationError("মোবাইল নম্বরটি ইতোমধ্যে রেজিস্টার্ড")
        return data


    def clean_nid(self):
        data = self.cleaned_data['nid']
        duplicate_nid = GuardianRegistration.objects.filter(nid=data)
        if self.instance.pk is not None:  # If you're editing an user, remove him from the duplicated results
            duplicate_nid = duplicate_nid.exclude(pk=self.instance.pk)
        if duplicate_nid.exists():
            raise forms.ValidationError("জাতীয় পরিচয়পত্র নম্বরটি ইতোমধ্যে রেজিস্টার্ড")
        return data


