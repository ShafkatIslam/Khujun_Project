from django.contrib import admin
from .models import Album, Song ,TeacherRegistration, GuardianRegistration, TeacherProfile, GuardianProfile, TuitionInfo

admin.site.register(Album)
admin.site.register(Song)
admin.site.register(TeacherRegistration)
admin.site.register(GuardianRegistration)
admin.site.register(TeacherProfile)
admin.site.register(GuardianProfile)
admin.site.register(TuitionInfo)