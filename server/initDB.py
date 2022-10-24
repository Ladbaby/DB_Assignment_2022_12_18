from django.db import connection
from django.conf import settings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

settings.configure(DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
})

with connection.cursor() as cursor:
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Artist(
                artistID INTEGER NOT NULL,
                artistName TEXT NOT NULL,
                PRIMARY KEY(artistID)
            );"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS User(
                userID INTEGER NOT NULL,
                userName TEXT NOT NULL,
                PRIMARY KEY(userID)
            );"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Album(
                albumID INTEGER NOT NULL,
                albumName TEXT NOT NULL,
                lastPlay INTEGER,
                uploaderID TEXT,
                granted INTEGER NOT NULL,
                artistID INTEGER NOT NULL,
                PRIMARY KEY(albumID),
                FOREIGN KEY(artistID) REFERENCES Artist(artistID) ON DELETE CASCADE
            );"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Track(
                trackID TEXT NOT NULL,
                trackName TEXT NOT NULL,
                trackLength REAL NOT NULL,
                trackIndex INTEGER NOT NULL,
                lastPlay INTEGER,
                albumID INTEGER NOT NULL,
                PRIMARY KEY(trackID),
                FOREIGN KEY(albumID) REFERENCES Album(albumID) ON DELETE CASCADE
            );"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Comment(
                commentID INTEGER NOT NULL,
                userID INTEGER NOT NULL,
                albumID INTEGER NOT NULL,
                content TEXT NOT NULL,
                PRIMARY KEY(commentID),
                FOREIGN KEY(userID) REFERENCES User(userID),
                FOREIGN KEY(albumID) REFERENCES Album(albumID) ON DELETE CASCADE
            );"""
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Collect(
                userID INTEGER NOT NULL,
                albumID INTEGER NOT NULL,
                PRIMARY KEY(userID, albumID),
                FOREIGN KEY(userID) REFERENCES User(userID),
                FOREIGN KEY(albumID) REFERENCES Album(albumID) ON DELETE CASCADE
            );"""
    )
    # cursor.execute(
    #     """CREATE TABLE IF NOT EXISTS Upload(
    #             userID TEXT NOT NULL,
    #             albumID TEXT NOT NULL,
    #             albumName TEXT NOT NULL,
    #             artistName TEXT NOT NULL,
    #             trackID TEXT NOT NULL,
    #             trackName TEXT NOT NULL,
    #             trackIndex INTEGER NOT NULL,
    #             granted INTEGER NOT NULL,
    #             PRIMARY KEY(userID, albumID, trackID),
    #             FOREIGN KEY(userID) REFERENCES User(userID)
    #         )"""
    # )
