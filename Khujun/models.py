from django.contrib.auth.models import Permission, User
from django.db import models


class Album(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    artist = models.CharField(max_length=250)
    album_title = models.CharField(max_length=500)
    genre = models.CharField(max_length=100)
    album_logo = models.FileField()
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.album_title + ' - ' + self.artist


class Song(models.Model):
    album = models.OneToOneField(Album, on_delete=models.CASCADE)
    song_title = models.CharField(max_length=250)
    audio_file = models.FileField(default='')
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.song_title

class TeacherRegistration(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True,)
    phone_number = models.IntegerField(max_length=11, blank=True)
    ssc_roll = models.IntegerField(max_length=6, blank=True)
    ssc_reg = models.IntegerField(max_length=10, blank=True)
    ssc_board = models.CharField(max_length=20, blank=True)
    verify = models.TextField(max_length=10, blank=True)
    otp = models.TextField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

class GuardianRegistration(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True,)
    phone_number = models.IntegerField(max_length=11, blank=True)
    nid = models.TextField(max_length=15, blank=True)
    verify = models.TextField(max_length=10, blank=True)
    otp = models.TextField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.TextField(max_length=50, blank=True)
    gender_name = models.CharField(max_length=200, blank=True)
    blood_group = models.CharField(max_length=200, blank=True)
    address = models.TextField(max_length=50, blank=True)
    city = models.TextField(max_length=50, blank=True)
    nid = models.TextField(max_length=17, blank=True)
    school = models.TextField(max_length=50, blank=True)
    college = models.TextField(max_length=50, blank=True)
    university = models.TextField(max_length=50, blank=True)
    subject = models.TextField(max_length=50, blank=True)
    experience = models.TextField(max_length=1000, blank=True)
    about = models.TextField(max_length=1000, blank=True)
    images = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.user.username

class GuardianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.TextField(max_length=50, blank=True)
    gender_name = models.CharField(max_length=200, blank=True)
    blood_group = models.CharField(max_length=200, blank=True)
    address = models.TextField(max_length=50, blank=True)
    city = models.TextField(max_length=50, blank=True)
    nid = models.TextField(max_length=17, blank=True)
    images = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.user.username
