from django.contrib.auth.models import Permission, User
from django.db import models
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError

def nid(value):
    if value < 0:
        raise ValidationError(
            ('Invalid'),
            params={'value': value},
        )


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
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.PositiveIntegerField(default=0,max_length=11, blank=True)
    ssc_roll = models.PositiveIntegerField(default=0,max_length=6,blank=True)
    ssc_reg = models.PositiveIntegerField(default=0,max_length=10,blank=True)
    ssc_board = models.CharField(max_length=20, blank=True)
    verify = models.TextField(max_length=10, blank=True)
    otp = models.TextField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

class GuardianRegistration(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True,)
    phone_number = models.PositiveIntegerField(default=0,max_length=11, blank=True)
    nid = models.BigIntegerField(default=0,max_length=17,blank=True,validators=[nid])
    verify = models.TextField(max_length=10, blank=True)
    otp = models.TextField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.TextField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    gender_group = models.CharField(max_length=200, blank=True)
    blood_group = models.CharField(max_length=200, blank=True)
    address = models.TextField(max_length=50, blank=True)
    city = models.TextField(max_length=50, blank=True)
    nid = models.BigIntegerField(default=0,max_length=17, blank=True,validators=[nid])
    school = models.TextField(max_length=50, blank=True)
    college = models.TextField(max_length=50, blank=True)
    university = models.TextField(max_length=50, blank=True)
    subject = models.TextField(max_length=50, blank=True)
    experience = models.TextField(max_length=1000, blank=True)
    about = models.TextField(max_length=1000, blank=True)
    images = models.TextField(max_length=1000, null=True, blank=True)
    notification = models.IntegerField(default=0)
    notifications = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class GuardianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, blank=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.TextField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True)
    gender_group = models.CharField(max_length=200, blank=True)
    blood_group = models.CharField(max_length=200, blank=True)
    address = models.TextField(max_length=50, blank=True)
    city = models.TextField(max_length=50, blank=True)
    nid = models.BigIntegerField(default=0,max_length=17, blank=True,validators=[nid])
    images = models.TextField(max_length=1000, null=True, blank=True)
    notification = models.IntegerField(default=0)
    notifications = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class TuitionInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_username = models.CharField(max_length=50, blank=True)
    teacher_firstname = models.CharField(max_length=50, blank=True)
    teacher_lastname = models.CharField(max_length=50, blank=True)
    classes = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=200, blank=True)
    day = models.CharField(max_length=200, blank=True)
    payment = models.TextField(max_length=50, blank=True)
    institute_name = models.TextField(max_length=50, blank=True)
    address = models.TextField(max_length=17, blank=True)
    teacher_confirm = models.IntegerField(default=0)
    guardian_confirm = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

class TeacherRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    teacher_username = models.CharField(max_length=50, blank=True)
    teacher_firstname = models.CharField(max_length=50, blank=True)
    teacher_lastname = models.CharField(max_length=50, blank=True)
    behaviour_rating = models.IntegerField(default=0)
    teaching_rating = models.IntegerField(default=0)
    response_rating = models.IntegerField(default=0)
    bio_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class Subscription(models.Model):
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=50, blank=True)

    def __str__(self):
        return self.name
