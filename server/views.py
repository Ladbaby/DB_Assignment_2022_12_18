import re
import sqlite3
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as Login
from django.contrib.auth import logout as Logout
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django import forms
import os
import json
import hashlib
from mutagen.mp3 import MP3

BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir)

# Create your views here.

@csrf_exempt
def index(request):
    file_name = 'index.html'
    file_path = os.path.join(os.path.join(BASE_DIR, "dist"), file_name)
    with open(file_path, 'r') as file:
        content = file.read()
        response = HttpResponse()
        response.write(content)
        return response

@csrf_exempt
def serve(request, folder, file_name):
    current_path = os.path.dirname(__file__)
    parent_path = os.path.abspath(os.path.join(current_path, os.pardir))
    dist_path = os.path.join(parent_path, 'dist')   
    if folder == 'js':
        folder_path = os.path.join(dist_path, 'js')
        content_type = 'text/javascript'
    elif folder == 'css':
        folder_path = os.path.join(dist_path, 'css')
        content_type = 'text/css'
    elif folder == 'img':
        folder_path = os.path.join(dist_path, 'img')
        content_type = 'img/png'
    else:
        pass
    file_path = os.path.join(folder_path, file_name)
    if folder == 'img':
        with open(file_path, 'rb') as file:
            content = file.read()
            response = HttpResponse()
            response['Content-Type'] = content_type
            response.write(content)
            return response
    else:
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            response = HttpResponse()
            response['Content-Type'] = content_type
            response.write(content)
            return response

@csrf_exempt
def register(request):
    length = int(request.headers.get('Content-Length'))
    request_content = json.loads(request.read(length).decode('utf-8'))
    try:
        user_name = request_content["auth"]["user-name"]
        pass_word = request_content["auth"]["password"]
    except (KeyError):
        return HttpResponse(status = 400)
    if User.objects.filter(username=user_name).exists():
        return HttpResponse(content = "user name already exists", status = 400)
    else:
        user = User.objects.create_user(username=user_name, password=pass_word)
        user.save()
        with connection.cursor() as cursor:
            sql = """INSERT INTO USER (userID, userName) VALUES (%s, %s)"""
            cursor.execute(sql, [str(user.id), user_name])
        return HttpResponse(status = 200)


@csrf_exempt
def login(request):
    length = int(request.headers.get('Content-Length'))
    request_content = json.loads(request.read(length).decode('utf-8'))
    try:
        username = request_content["auth"]["user-name"]
        password = request_content["auth"]["password"]
    except KeyError:
        return HttpResponse(status = 400)
    user = authenticate(username = username, password = password)
    if user is not None:
        Login(request, user)
        if request.user.is_staff:
            response_content = {"isAdmin": True}
        else:
            response_content = {"isAdmin": False}
        return JsonResponse(response_content, status = 200)
    else:
        return HttpResponse(status = 403)


@csrf_exempt
def logout(request):
    Logout(request)
    return HttpResponse(status = 200)


@csrf_exempt
def search_artist(request):
    # if request.user.is_authenticated:
        artist_name = request.GET.get('target')
        if artist_name is not None:
            with connection.cursor() as cursor:
                sql = """SELECT albumID
                FROM Artist INNER JOIN Album ON Artist.artistID = Album.artistID 
                WHERE artistName = %s AND album.granted = 1"""
                result = cursor.execute(sql, [artist_name,]).fetchall()

                if not result:
                    return JsonResponse({"albums": []}, status = 200)

                albumID = []
                for row in result:
                    albumID.append(row[0])

            Albums = check_album_utility(albumID)

            return JsonResponse({"albums": Albums}, status = 200)
        else:
            return HttpResponse(status = 400)

    # else:
        # return HttpResponse(status = 403)


@csrf_exempt
def search_albumID(request):
    # if request.user.is_authenticated:
        album_id = request.GET.get('target')
        albumID = []
        if album_id is not None:
            if album_id == '':
                return HttpResponse(status = 400)
            else:
                albumID.append(album_id)
        else:
            with connection.cursor() as cursor:
                sql = """SELECT albumID from Album Where Album.granted = 1"""
                result = cursor.execute(sql).fetchall()

                if not result:
                    return JsonResponse({"albums": []}, status = 200)

                for row in result:
                    albumID.append(row[0])
        
        Albums = check_album_utility(albumID)
    
        return JsonResponse({"albums": Albums}, status = 200)
    # else:
        # return HttpResponse(status=403)


@csrf_exempt
def search_albumName(request):
    # if request.user.is_authenticated:
        album_name = request.GET.get('target')
        if album_name is not None:
            albumID = []
            with connection.cursor() as cursor:
                sql = """SELECT albumID FROM Album WHERE albumName = %s AND album.granted = 1"""
                result = cursor.execute(sql, [album_name,]).fetchall()

                if not result:
                    return JsonResponse({"albums": []}, status = 200)

                for row in result:
                    albumID.append(row[0])

            Albums = check_album_utility(albumID)

            return JsonResponse({"albums": Albums}, status = 200)
        else:
            return HttpResponse(status = 400)
    # else:
    #     return HttpResponse(status=403)

@csrf_exempt
def check_collection(request):
    if request.user.is_authenticated:
        user_id = request.user.id

        albumID = []
        with connection.cursor() as cursor:
            sql = """SELECT albumID from Collect Where userID = %s"""
            result = cursor.execute(sql, [user_id,]).fetchall()

            if not result:
                return JsonResponse({"albums": []}, status = 200)

            for row in result:
                albumID.append(row[0])
        
        Albums = check_album_utility(albumID)
    
        return JsonResponse({"albums": Albums}, status = 200)
    else:
        return HttpResponse(status = 403)

@csrf_exempt
def add_album_to_collection(request):
    # if request.user.is_authenticated:
        length = int(request.headers.get('Content-Length'))
        request_content = json.loads(request.read(length).decode('utf-8'))
        try:
            album_id = request_content["id"]
        except KeyError:
            return HttpResponse(status = 400)
        user_id = request.user.id
        with connection.cursor() as cursor:
            sql = """INSERT INTO Collect (userID, albumID) VALUES (%s, %s)"""
            try:
                cursor.execute(sql, [user_id, album_id])
            except sqlite3.Error as er:
                return HttpResponse(content = "album not exist", status = 400)
        return HttpResponse(status = 200)
    # else:
    #     return HttpResponse(status = 403)


@csrf_exempt
def remove_album_from_collection(request):
    # if request.user.is_authenticated:
        length = int(request.headers.get('Content-Length'))
        request_content = json.loads(request.read(length).decode('utf-8'))
        try:
            album_id = request_content["id"]
        except KeyError:
            return HttpResponse(status = 400)
        user_id = request.user.id
        with connection.cursor() as cursor:
            sql = """DELETE FROM Collect Where userID = %s AND albumID = %s"""
            try:
                cursor.execute(sql, [user_id, album_id])
            except sqlite3.Error as er:
                return HttpResponse(content = "album not exist", status = 400)
        return HttpResponse(status = 200)
    # else:
    #     return HttpResponse(status = 403)


@csrf_exempt
def play_track(request):
    # if request.user.is_authenticated:
        track_id = request.GET.get('target')
        if track_id is not None:
            with connection.cursor() as cursor:
                sql = """SELECT trackName, trackLength, lastPlay, trackID
                FROM Track WHERE Track.trackID = %s"""
                result = cursor.execute(sql, [track_id,]).fetchone()

                if result is None:
                    return HttpResponse(content = "track not exist", status = 400)

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
                return JsonResponse(response_content, status = 200)
        else:
            return HttpResponse(status = 400)
    # else:
    #     return HttpResponse(status = 403)

@csrf_exempt
def send_music(request):
    # if request.user.is_authenticated:
        song_name = request.GET.get('s')
        if song_name is not None:
            song_name += '.mp3'
            current_path = os.path.dirname(__file__)
            song_path = os.path.join(os.path.join(current_path, "music"), song_name)
            with open(song_path, "rb") as song_file:
                response = HttpResponse()
                response['Content-Type']='audio/mp3'
                response['Content-Length']=os.path.getsize(song_path)
                response.write(song_file.read())
                return response
        else:
            return HttpResponse(status = 400)
    # else:
    #     return HttpResponse(status = 403)


@csrf_exempt
def track_lastplay(request):
    # if request.user.is_authenticated:
        length = int(request.headers.get('Content-Length'))
        request_content = json.loads(request.read(length).decode('utf-8'))
        try:
            track_id = request_content["id"]
            time = request_content["time"]
        except KeyError:
            return HttpResponse(status = 400)

        with connection.cursor() as cursor:
            sql = """UPDATE Track SET lastPlay = %s
            WHERE trackID = %s"""
            try:
                cursor.execute(sql, [time, track_id])
            except sqlite3.Error as er:
                return HttpResponse(content = "track not exist", status = 400)

        return HttpResponse(status = 200)
    # else:
    #     return HttpResponse(status = 403)

@csrf_exempt
def upload(request):
    # if request.user.is_authenticated:
        return upload_utility(request, False)
    # else:
    #     return HttpResponse(status = 403)


@csrf_exempt
def comment(request):
    # if request.user.is_authenticated:
        user_id = request.user.id
        length = int(request.headers.get('Content-Length'))
        resposne_content = json.loads(request.read(length).decode('utf-8'))

        try:
            album_id = resposne_content["id"]
            comment_content = resposne_content["comment"]
        except KeyError:
            return HttpResponse(status = 400)

        with connection.cursor() as cursor:
            sql = """SELECT MAX(commentID) FROM Comment"""
            current_id = cursor.execute(sql).fetchone()
            if current_id is None:
                comment_id = 1
            else:
                comment_id = current_id[0] + 1

        with connection.cursor() as cursor:
            sql = """INSERT INTO Comment(commentID, userID, albumID, content)
            VALUES (%s, %s, %s, %s)"""
            try:
                cursor.execute(sql, [comment_id, user_id, album_id, comment_content])
            except:
                print("insert into comment fail")
                return HttpResponse(status = 400)
        return HttpResponse(status = 200)
    # else:
    #     return HttpResponse(status = 403)


@csrf_exempt
def check_upload(request):
    # if request.user.is_authenticated:
        user_id = request.user.id
        with connection.cursor() as cursor:
            sql = """SELECT albumName, granted FROM Album
            WHERE uploaderID = %s"""
            result = cursor.execute(sql, [user_id,]).fetchall()

            if not result:
                return JsonResponse({"notification": []}, status = 200)

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
            
            return JsonResponse({"notification": notification}, status = 200)
    # else:
    #     return HttpResponse(status = 403)

@csrf_exempt
def admin_upload(request):
    # if request.user.is_authenticated:
        if request.user.is_staff:
            return upload_utility(request, True)
        else:
            return HttpResponse(status = 403)
    # else:
    #     return HttpResponse(stauts = 403)


@csrf_exempt
def admin_remove(request):
    # if request.user.is_authenticated:
        if request.user.is_staff:
            length = int(request.headers.get('Content-Length'))
            request_content = json.loads(request.read(length).decode('utf-8'))
            try:
                album_ID = request_content["id"]
            except KeyError:
                return HttpResponse(status = 400)

            with connection.cursor() as remove_track:
                sql = """SELECT trackID FROM Track Where albumID = %s"""

                result = remove_track.execute(sql, [album_ID,])

                for row in result:
                    track_id = row[0]
                    file_path = os.path.join(os.path.join(os.path.join(BASE_DIR, "server"), "music"), track_id+".mp3")
                    os.remove(file_path)

            with connection.cursor() as cursor:
                sql = """DELETE FROM Album WHERE albumID=%s"""

                try:
                    cursor.execute(sql, [album_ID,])
                except sqlite3.Error as er:
                    print("admin remove album fail")
                    return HttpResponse(status = 400)

            return HttpResponse(status = 200)
        else:
            return HttpResponse(status = 403)
    # else:
    #     return HttpResponse(status = 403)


@csrf_exempt
def admin_check_upload(request):
    # if request.user.is_authenticated:
        if request.user.is_staff:
            upload_list = []
            with connection.cursor() as cursor:
                sql = """SELECT albumID FROM Album WHERE granted = 0"""
                uploads = cursor.execute(sql).fetchall()

                if not uploads:
                    return JsonResponse({"upload": []}, status = 200)

                for upload in uploads:
                    album_id = upload[0]

                    upload_info = {}
                    with connection.cursor() as cursor_select_album:
                        sql_select_album = """SELECT userID, userName, albumName, artistName, trackID, trackName
                        FROM User INNER JOIN Album ON User.userID = Album.uploaderID
                        INNER JOIN Artist ON Album.artistID = Artist.artistID
                        INNER JOIN Track ON Album.albumID = Track.albumID
                        WHERE Album.albumID = %s"""

                        try:
                            tracks = cursor_select_album.execute(sql_select_album, [album_id,]).fetchall()
                        except sqlite3.Error as er:
                            print("admin check upload error")
                            return HttpResponse(status = 400)

                        if not tracks:
                            continue

                        track_list = []
                        for track in tracks:
                            track_ID = track[4]
                            track_name = track[5]
                            track_list.append({"trackID": track_ID, "trackName": track_name}) 
                        upload_info['userID'] = tracks[0][0]
                        upload_info['userName'] = tracks[0][1]
                        upload_info['album'] = {'id': album_id, 'name': tracks[0][2], 'artsit': tracks[0][3], 'tracks': track_list}
                    upload_list.append(upload_info)
            return JsonResponse({"upload": upload_list}, status = 200)
        else:
            return HttpResponse(status = 403)
    # else:
    #     return HttpResponse(status = 403)


@csrf_exempt
def admin_reply(request):
    # if request.user.is_authenticated:
        if request.user.is_staff:
            length = int(request.headers.get('Content-Length'))
            request_content = json.loads(request.read(length).decode('utf-8'))

            try:
                replies = request_content['reply']
            except KeyError:
                return HttpResponse(status = 400)

            for reply in replies:

                try:
                    album_ID = reply['albumID']
                    success = reply['success']
                except KeyError:
                    return HttpResponse(status = 400)

                with connection.cursor() as cursor:
                    sql = """UPDATE Album SET granted = %s WHERE albumID = %s"""
                    try:
                        cursor.execute(sql, [success, album_ID])
                    except sqlite3.Error as er:
                        print("update admin reply fail")
                        return HttpResponse(status = 400)

            return HttpResponse(status = 200)
        else:
            return HttpResponse(status = 403)
    # else:
    #     return HttpResponse(status = 403)

@csrf_exempt
def check_album_utility(album_id_list):

    Albums = []

    for album_id in album_id_list:
        with connection.cursor() as cursor:
            sql = """SELECT Album.albumID, albumName, artistName, trackID, trackName
            FROM Artist INNER JOIN Album ON Artist.artistID = Album.artistID 
            INNER JOIN Track ON Album.albumID = Track.albumID
            Where Album.albumID = %s AND album.granted = 1"""
            result = cursor.execute(sql, [album_id,]).fetchall() 

        with connection.cursor() as cursor:
            sql = """SELECT Comment.userID, userName, content
            FROM Comment INNER JOIN User ON User.userID = Comment.userID
            WHERE Comment.albumID = %s"""
            comment_result = cursor.execute(sql, [album_id,]).fetchall()

        tracks = []
        for row in result:
            trackinfo={}
            trackinfo['trackID'] = row[3]
            trackinfo['trackName'] = row[4]
            tracks.append(trackinfo)
        comments = []

        for row in comment_result:
            comment_info = {}
            comment_info['userID']=row[0]
            comment_info['userName']=row[1]
            comment_info['comment']=row[2]
            comments.append(comment_info)

        currentAlbum = {"id": result[0][0],"name": result[0][1], "artist": result[0][2], "tracks": tracks, "comments": comments}
        Albums.append(currentAlbum)
    
    return Albums

@csrf_exempt
def upload_utility(request, if_admin):

    grant = 0
    if if_admin:
        grant = 1

    album_name = request.POST.get('name')
    artist_name = request.POST.get('artist')

    if album_name is None or artist_name is None:
        return HttpResponse(status = 400)

    artist_ID = ""

    # insert into table artist
    with connection.cursor() as cursor:
        sql_check_existence = """SELECT Artist.artistID
        From Artist INNER JOIN Album on Artist.artistID = Album.artistID
        WHERE Artist.artistName = %s AND (Album.granted = 1 OR Album.granted = 0)"""
        result = cursor.execute(sql_check_existence, [artist_name,]).fetchall()

        if not result:

            with connection.cursor() as cursor_get_id:
                max_artistID = cursor_get_id.execute("SELECT MAX(artistID) FROM Artist").fetchone()
                if max_artistID is None:
                    artist_ID = 1
                else:
                    artist_ID = int(max_artistID[0]) + 1

            with connection.cursor() as cursor_insert_artist:
                try:
                    sql_insert_artist = """INSERT INTO Artist(artistID, artistName) VALUES (%s, %s)"""
                except sqlite3.Error as er:
                    print("upload album, insert into artist fail")
                    return HttpResponse(status = 400)

                cursor_insert_artist.execute(sql_insert_artist, [artist_ID, artist_name])

        else:
            artist_ID = result[0][0]

    user_ID = str(request.user.id)

    # insert into table album
    with connection.cursor() as cursor:
        max_albumID = cursor.execute("SELECT MAX(albumID) FROM Album").fetchone()
        if max_albumID is None:
            album_ID = 1
        else:
            album_ID = int(max_albumID[0]) + 1

    with connection.cursor() as cursor:
        sql = """INSERT INTO Album(albumID, albumName, uploaderID, granted, artistID)
        VALUES (%s, %s, %s, %s, %s)"""
        try:
            cursor.execute(sql, [album_ID, album_name, user_ID, grant, artist_ID])
        except sqlite3.Error as er:
            print("upload album, insert into album fail")
            return HttpResponse(status = 400)

    track_index = 1
    current_path = os.path.dirname(__file__)

    for track in request.FILES.lists():

        try:
            track_name = track[0]
            track_files = track[1]
        except KeyError:
            return HttpResponse(stauts = 400)

        for track_file in track_files:

            file_content = track_file.read()
            md5 = hashlib.md5()
            md5.update(file_content)
            track_ID = md5.hexdigest()

            new_file_path = os.path.join(os.path.join(current_path, "music"), track_ID+".mp3")
            with open(new_file_path, 'wb') as newfile:
                newfile.write(file_content)

            audio = MP3(track_file)
            track_length = audio.info.length
            # insert into table track
            with connection.cursor() as cursor:
                sql = """INSERT INTO Track(trackID, trackName, trackLength, trackIndex, albumID)
                VALUES (%s, %s, %s, %s, %s)"""
                try:
                    cursor.execute(sql, [track_ID, track_name, track_length, track_index, album_ID])
                except sqlite3.Error as er:
                    print("upload album, insert track fail")
                    return HttpResponse(status = 400)
            track_index+=1

    
    return HttpResponse(status = 200)
