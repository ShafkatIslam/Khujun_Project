from django.conf.urls import url
from Khujun import views
from django.conf import settings
from django.conf.urls.static import static
# SET THE NAMESPACE!
app_name = 'Khujun'


urlpatterns = [
    url(r'^$', views.mainlogin, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^registers/$', views.registers, name='registers'),
    url(r'^mainreg/$', views.mainreg, name='mainreg'),
    url(r'^mainlogin/$', views.mainlogin, name='mainlogin'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^login_users/$', views.login_users, name='login_users'),
    url(r'^teacher_profile_edit/$', views.teacher_profile_edit, name='teacher_profile_edit'),
    url(r'^teacher_image_edit/$', views.teacher_image_edit, name='teacher_image_edit'),
    url(r'^guardian_profile_edit/$', views.guardian_profile_edit, name='guardian_profile_edit'),
    url(r'^guardian_image_edit/$', views.guardian_image_edit, name='guardian_image_edit'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<song_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^create_album/$', views.create_album, name='create_album'),
    url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    url(r'^(?P<album_id>[0-9]+)/favorite_album/$', views.favorite_album, name='favorite_album'),
    url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)