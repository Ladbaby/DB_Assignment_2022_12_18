import re
import sqlite3
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
import os
import json
import hashlib
from mutagen.mp3 import MP3

# Create your views here.

globalAlbumID = 1
globalArtistID = 1

@csrf_exempt
def index(request):
    return HttpResponse("""<button>upload</button>
<script>
    let button_upload = document.querySelector('button')
    button_upload.addEventListener('click', function(){
    var formData = new FormData()
    formData.append("name", "jntm")
    formData.append("artist", "cxk")
    formData.append("rap", "xxx")
    formData.append("basketball", "xxx")
    let req = new XMLHttpRequest()
    req.open('POST', 'upload/')
    req.send(formData)
    })
</script>""")


def register(request):
    length = int(request.headers.get('Content-Length'))
    request_content = json.loads(request.read(length).decode('utf-8'))
    username = request_content["auth"]["user-name"]
    password = request_content["auth"]["password"]
    if User.objects.filter(username=username).exists():
        return HttpResponse(status = 400)
    else:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        with connection.cursor() as cursor:
            sql = """INSERT INTO USER (userID, userName) VALUES (%s, %s)"""
            cursor.execute(sql, [str(user.id), username])
    return HttpResponse(status = 200)

@csrf_exempt
def login(request):
    length = int(request.headers.get('Content-Length'))
    request_content = json.loads(request.read(length).decode('utf-8'))
    username = request_content["auth"]["user-name"]
    password = request_content["auth"]["password"]
    user = authenticate(username = username, password = password)
    if user is not None:
        login(request, user)
        return HttpResponse(status = 200)
    else:
        return HttpResponse(status = 403)

def search_artist(request):
    if request.user.is_authenticated:
        artist_name = request.GET.get('target')
        with connection.cursor() as cursor:
            sql = """SELECT albumID, albumName
            FROM Artist INNER JOIN Album ON Artist.artistID = Album.artistID 
            WHERE artistName = %s AND album.granted = 1"""
            result = cursor.execute(sql, [artist_name,]).fetchall()
            albums = []
            for row in result:
                albuminfo={}
                albuminfo['albumID'] = row[0]
                albuminfo['albumName'] = row[1]
                albums.append(albuminfo)
            response_content = {"albums": albums}
            response = JsonResponse(response_content)
            response.status_code = 200
            return response
    else:
        return HttpResponse(status = 403)

def search_albumID(request):
    if request.user.is_authenticated:
        album_id = request.GET.get('target')
        with connection.cursor() as cursor:
            sql = """SELECT albumName, artistName, trackID, trackName
            FROM Artist INNER JOIN Album ON Artist.artistID = Album.artistID INNER JOIN Track ON Album.albumID = Track.albumID
            Where Album.albumID = %s AND album.granted = 1"""
            result = cursor.execute(sql, [album_id,]).fetchall()
            tracks = []
            for row in result:
                trackinfo={}
                trackinfo['trackID'] = row[2]
                trackinfo['trackName'] = row[3]
                tracks.append(trackinfo)
            response_content = {"name": result[0][0], "artist": result[0][1], "tracks": tracks}
            response = JsonResponse(response_content)
            response.status_code = 200
            return response
    else:
        return HttpResponse(status=403)

def search_albumName(request):
    if request.user.is_authenticated:
        album_name = request.GET.get('target')
        albums = []
        with connection.cursor() as cursor:
            sql = """SELECT albumID FROM Album WHERE albumName = %s AND album.granted = 1"""
            result = cursor.execute(sql, [album_name,]).fetechall()
            for row in result:
                album_ID = row[0]
                with connection.cursor() as cursor1:
                    sql = """SELECT artistName, trackID, trackName
                    FROM Artist INNER JOIN Album ON Artist.artistID = Album.artistID INNER JOIN Track ON Album.albumID = Track.albumID
                    WHERE Album.albumID = %s"""
                    result_tracks = cursor1.execute(sql, [album_ID,]).fetchall()

                    album_info = {}
                    album_info['id'] = album_ID
                    album_info['name'] = album_name
                    album_info['artist'] = result_tracks[0][0]
                    track_list = []
                    for result_track in result_tracks:
                        track_ID = result_track[1]
                        track_name = result_track[2]
                        track_info = {"trackID": track_ID, "trackName": track_name}
                        track_list.append(track_info)
                    album_info['tracks'] = track_list
                albums.append(album_info)
        response = JsonResponse(albums)
        response.status_code = 200
        return response
    else:
        return HttpResponse(status=403)

def add_album_to_collection(request):
    if request.user.is_authenticated:
        album_id = request.POST.get('target')
        user_id = request.user.id
        with connection.cursor() as cursor:
            sql = """INSERT INTO Collect (userID, albumID) VALUES (%s, %s)"""
            cursor.execute(sql, [user_id, album_id])
        return HttpResponse(status = 200)
    else:
        return HttpResponse(status = 403)

def remove_album_from_collection(request):
    if request.user.is_authenticated:
        album_id = request.POST.get('target')
        user_id = request.user.id
        with connection.cursor() as cursor:
            sql = """DELETE FROM Collect Where userID = %s AND albumID = %s"""
            cursor.execute(sql, [user_id, album_id])
        return HttpResponse(status = 200)
    else:
        return HttpResponse(status = 403)

def play_track(request):
    if request.user.is_authenticated:
        track_id = request.GET.get('target')
        with connection.cursor() as cursor:
            sql = """SELECT trackName, trackLength, lastPlay, trackID
            FROM Track WHERE Track.trackID = %s"""
            result = cursor.execute(sql, [track_id,]).fetchone()
            track_url = "/music?s="+result[3]
            if result[2] is None:
                lastplay = -1
            else:
                lastplay = result[2]
            response_content = {
                "name": result[0],
                "length": result[1], 
                "lastPlay": lastplay,
                "url": track_url
            }
            response = JsonResponse(response_content)
            response.status_code = 200
            return response
    else:
        return HttpResponse(status = 403)
    # return HttpResponse("""<audio controls>
    # <source src="/music?s=Airbus.mp3" type="audio/mp3">
    # </audio>""", content_type='text/html')

def send_music(request):
    if request.user.is_authenticated:
        song_name = request.GET.get('s')
        current_path = os.path.dirname(__file__)
        file_path = os.path.join(current_path, 'music/'+song_name+'.mp3')
        with open(file_path, "rb") as song_file:
            response = HttpResponse()
            response['Content-Type']='audio/mp3'
            response['Content-Length']=os.path.getsize(file_path)
            response.write(song_file.read())
            return response
    else:
        return HttpResponse(status = 403)
    # song_name = request.GET.get('s')
    # current_path = os.path.dirname(__file__)
    # file_path = os.path.join(current_path, 'music/Airbus.mp3')
    # with open(file_path, "rb") as song_file:
    #     response = HttpResponse()
    #     response['Content-Type']='audio/mp3'
    #     response['Content-Length']=os.path.getsize(file_path)
    #     response.write(song_file.read())
    #     return response

def track_lastplay(request):
    if request.user.is_authenticated:
        track_id = request.POST.get('target')
        time = int(request.POST.get('time'))
        with connection.cursor() as cursor:
            sql = """UPDATE Track SET lastPlay = %d
            WHERE trackID = %s"""
            cursor.execute(sql, [time, track_id])
        return HttpResponse(status = 200)
    else:
        return HttpResponse(status = 403)

@csrf_exempt
def upload(request):
    if request.user.is_authenticated:
        _upload(request, False)
        return HttpResponse(status = 200)
    else:
        return HttpResponse(status = 403)

def comment(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        album_id = request.POST.get('target')
        length = request.headers.get('Content-Length')
        comment_content = request.read(length).decode('utf-8')
        with connection.cursor() as cursor:
            sql = """INSERT INTO Comment(userID, albumID, content)
            VALUES (%s, %s, %s)"""
            cursor.execute(sql, [user_id, album_id, comment_content])
        return HttpResponse(status = 200)
    else:
        return HttpResponse(status = 403)

def check_upload(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        with connection.cursor() as cursor:
            sql = """SELECT albumName, granted FROM Album
            WHERE uploaderID = %s"""
            result = cursor.execute(sql, [user_id,]).fetchall()
            notification = []
            for row in result:
                check_content = {}
                check_content['albumName'] = row[0]
                if row[1] == 1:
                    check_content['status'] = "success"
                elif row[1] == 0:
                    check_content['status'] = "waiting"
                elif row[1] == -1:
                    check_content['status'] = "fail"
                else:
                    pass
                notification.append(check_content)
            response_content = {"notication": notification}
            response = JsonResponse(response_content)
            response.status_code = 200
            return response
    else:
        return HttpResponse(status = 403)

def admin_upload(request):
    if request.user.is_authenticated:
        if request.user.is_stuff:
            _upload(request, True)
            return HttpResponse(status = 200)
        else:
            return HttpResponse(status = 403)
    else:
        return HttpResponse(stauts = 403)

def admin_remove(request):
    if request.user.is_authenticated:
        if request.user.is_stuff:
            album_ID = request.POST.get('target')
            with connection.cursor() as cursor:
                sql = """DELETE FROM Album WHERE albumID=%s"""
                cursor.execute(sql, [album_ID,])
            return HttpResponse(status = 200)
        else:
            return HttpResponse(status = 403)
    else:
        return HttpResponse(status = 403)

def admin_check_upload(request):
    if request.user.is_authenticated:
        if request.user.is_stuff:
            upload_list = []
            with connection.cursor() as cursor:
                sql = """SELECT albumID FROM Album WHERE granted = 0"""
                uploads = cursor.execute(sql).fetchall()
                for upload in uploads:
                    album_id = upload[0]
                    upload_info = {}
                    with connection.cursor() as cursor1:
                        sql = """SELECT userID, userName, albumName, artistName, trackID, trackName
                        FROM User INNER JOIN Album ON User.userID = Album.uploaderID
                        INNER JOIN Artist ON Album.artistID = Artist.artistID
                        INNER JOIN Track ON Album.albumID = Track.albumID
                        WHERE albumID = %s"""
                        tracks = cursor1.execute(sql, [album_id,]).fetchall()
                        track_list = []
                        for track in tracks:
                            track_ID = track[4]
                            track_name = track[5]
                            track_list.append({"trackID": track_ID, "trackName": track_name}) 
                        upload_info['userID'] = tracks[0][0]
                        upload_info['userName'] = tracks[0][1]
                        upload_info['album'] = {'id': album_id, 'name': tracks[0][2], 'artsit': tracks[0][3], 'tracks': track_list}
                    upload_list.append(upload_info)
            response = JsonResponse(upload_list)
            response.status_code = 200
            return response
        else:
            return HttpResponse(status = 403)
    else:
        return HttpResponse(status = 403)

def admin_reply(request):
    if request.user.is_authenticated:
        if request.user.is_stuff:
            length = int(request.headers.get('Content-Length'))
            request_content = json.loads(request.read(length).decode('utf-8'))
            replies = request['reply']
            for reply in replies:
                album_ID = reply['albumID']
                success = reply['success']
                if success == 0:
                    success = -1
                with connection.cursor() as cursor:
                    sql = """UPDATE Album SET granted = %d WHERE albumID = %s"""
                    cursor.execute(sql, [success, album_ID])
            return HttpResponse(status = 200)
        else:
            return HttpResponse(status = 403)
    else:
        return HttpResponse(status = 403)







def _upload(request, if_admin):
    grant = 0
    if if_admin:
        grant =1

    post_content = request.POST.copy()
    album_name = post_content.get('name')
    artist_name = post_content.get('artist')
    artist_ID = ""
    new_artist = False

    # insert into table artist
    with connection.cursor() as cursor:
        sql_check_existence = """SELECT COUNT(*)
        From Artist INNER JOIN Album on Artist.artistID = Album.artistID
        WHERE Artist.artistName = %s AND (Album.granted = 1 OR Album.granted = 0)"""
        result = cursor.execute(sql_check_existence, [artist_name,])
        if result == 0:
            artist_ID = globalArtistID
            globalArtistID += 1
            sql_insert_artist = """INSERT INTO Artist(artistID, artistName) VALUES (%s, %s)"""
            with connection.cursor() as cursor1:
                cursor1.execute(sql_insert_artist, [artist_ID, artist_name])
        else:
            sql_getID = """SELECT artistID FROM Artist WHERE artistName = %s"""
            with connection.cursor() as cursor2:
                artist_ID = cursor.execute(sql_getID, [artist_name,]).fetchone()[0]
    user_ID = request.user.id
    album_ID = globalAlbumID
    globalAlbumID += 1

    # insert into table album
    with connection.cursor() as cursor:
        sql = """INSERT INTO Album(albumID, albumName, uploaderID, granted)
        VALUES (%s, %s, %s, %d)"""
        cursor.execute(sql, [album_ID, album_name, user_ID, grant])
    track_index = 1
    current_path = os.path.dirname(__file__)
    post_content.pop('name')
    post_content.pop('artist')
    track_list = post_content.lists()
    for track in track_list:
        track_name = track[0]
        track_files = track[1]
        for track_file in track_files:
            file_content = track_file.read()
            md5 = hashlib.md5()
            md5.update(file_content)
            track_ID = md5.hexdigest()
            new_file_path = os.path.join(current_path, "music/"+track_ID+".mp3")
            with open(new_file_path, 'wb') as newfile:
                newfile.write(file_content)
            audio = MP3(track_file)
            track_length = audio.info.length
            # insert into table track
            with connection.cursor() as cursor:
                sql = """INSERT INTO Track(trackID, trackName, trackLength, trackIndex)
                VALUES (%s, %s, %d, %d)"""
                cursor.execute(sql, [track_ID, track_name, track_length, track_index])
            
            track_index+=1
