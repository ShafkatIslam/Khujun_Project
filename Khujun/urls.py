from django.conf.urls import url
from Khujun import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
# SET THE NAMESPACE!
app_name = 'Khujun'

#handler404 = 'Khujun.views.handler404'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^registers/$', views.registers, name='registers'),
    url(r'^mainreg/$', views.mainreg, name='mainreg'),
    url(r'^mainlogin/$', views.mainlogin, name='mainlogin'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^login_users/$', views.login_users, name='login_users'),
    url(r'^subscribe/$', views.subscribe, name='subscribe'),
    url(r'^teacher_profile_edit/$', views.teacher_profile_edit, name='teacher_profile_edit'),
    url(r'^teacher_image_edit/$', views.teacher_image_edit, name='teacher_image_edit'),
    url(r'^guardian_profile_edit/$', views.guardian_profile_edit, name='guardian_profile_edit'),
    url(r'^guardian_image_edit/$', views.guardian_image_edit, name='guardian_image_edit'),
    url(r'^teacher_dashboard/$', views.teacher_dashboard, name='teacher_dashboard'),
    url(r'^(?P<id>[0-9]+)/teachersprofile/$', views.teachersprofile, name='teachersprofile' ),
    url(r'^guardian_dashboard/$', views.guardian_dashboard, name='guardian_dashboard'),
    url(r'^(?P<id>[0-9]+)/teacherprofile/$', views.teacherprofile, name='teacherprofile' ),
    url(r'^teacherrating/(?P<id>[0-9]+)/$', views.teacherrating, name='teacherrating' ),
    url(r'^teacherrequests/(?P<id>[0-9]+)/$', views.teacherrequests, name='teacherrequests' ),
    url(r'^teacher_notification/$', views.teacher_notification, name='teacher_notification'),
    url(r'^details_tuition_info/(?P<id>[0-9]+)/$', views.details_tuition_info, name='details_tuition_info' ),
    url(r'^teacher_accept/(?P<id>[0-9]+)/$', views.teacher_accept, name='teacher_accept' ),
    url(r'^teacher_reject/(?P<id>[0-9]+)/$', views.teacher_reject, name='teacher_reject' ),
    url(r'^guardian_notification/$', views.guardian_notification, name='guardian_notification'),
    url(r'^details_tuitions_info/(?P<id>[0-9]+)/$', views.details_tuitions_info, name='details_tuitions_info' ),
    url(r'^guardian_accept/(?P<id>[0-9]+)/$', views.guardian_accept, name='guardian_accept' ),
    url(r'^guardian_reject/(?P<id>[0-9]+)/$', views.guardian_reject, name='guardian_reject' ),
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