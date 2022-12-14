from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    re_path(r"^(js|css|img)\/(.*)$", views.serve),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout")
]

urlpatterns += [
    path('search-artist/', views.search_artist, name="search-artist"),
    path('search-album-id/', views.search_albumID, name="search-album-id"),
    path('search-album-name/', views.search_albumName, name="search-album-name"),
]

urlpatterns += [
    path('check-collection/', views.check_collection, name="check-collection"),
    path('add-album/', views.add_album_to_collection, name="add-album"),
    path('remove-album/', views.remove_album_from_collection, name="remove-album"),
]

urlpatterns += [
    path('play/', views.play_track, name="play"),
    path('music/', views.send_music, name="music"),
    path('track-lastplay/', views.track_lastplay, name="track-lastplay")
]

urlpatterns += [
    path('upload/', views.upload, name="upload"),
    path('check-upload-notification/', views.check_upload, name="check-upload-notification")
]

urlpatterns += [
    path('comment/', views.comment, name="comment")
]

urlpatterns += [
    path('admin/upload/', views.admin_upload, name="admin-upload"),
    path('admin/remove/', views.admin_remove, name="admin-remove")
]

urlpatterns += [
    path('admin/check-upload/', views.admin_check_upload, name="admin-check-upload"),
    path('admin/reply/', views.admin_reply, name = "admin-reply")
]