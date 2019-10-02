from django.contrib import admin
from .models import Album, Song ,TeacherRegistration, GuardianRegistration

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(TeacherRegistration)
admin.site.register(GuardianRegistration)