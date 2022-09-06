[toc]
## 1. Users

### 1.1. users register

##### 1.1.0.1. Request

POST '/register'

```json{.line-numbers}
{
    "auth" : {
        "user-name" : "xxx",
        "password" : "xxx"
    }
}
```

##### 1.1.0.2. Response

200 OK

Set-Cookie: session=xxx

### 1.2. users login

##### 1.2.0.1. Request

POST '/login'

```json{.line-numbers}
{
    "auth" : {
        "user-name" : "xxx",
        "password" : "xxx"
    }
}
```

##### 1.2.0.2. Response

200 OK

```json{.line-numbers}
{
    "login-status" : "1/0"
}
```

### 1.3. users search artists

##### 1.3.0.1. Request

GET '/search-artist?target=artist-name'  

##### 1.3.0.2. Response

200 OK

```json{.line-numbers}
{
    "albums" : [
        {"albumID" : "xxx", "albumName" : "xxx"},
        {"albumID" : "xxx", "albumName" : "xxx"},
    ]
}

```

### 1.4. users search album by album id

##### 1.4.0.1. Request 

GET '/search-album-id?target=album-id'

##### 1.4.0.2. Response

```json{.line-numbers}
{
    "name" : "xxx",
    "artist" : "xxx",
    "tracks" : [
        {"trackID" : "xxx", "trackName" : "xxx"},
        {"trackID" : "xxx", "trackName" : "xxx"}
    ]
}
```

### 1.5. users search albums by name

##### 1.5.0.1. Request

GET '/search-album-name?target=album-name'

##### 1.5.0.2. Response

200 OK

```json{.line-numbers}
{
    "name" : "xxx",
    "artist" : "xxx",
    "tracks" : [
        {"trackID" : "xxx", "trackName" : "xxx"},
        {"trackID" : "xxx", "trackName" : "xxx"}
    ]
}
```

### 1.6. users add album to personal collection

##### 1.6.0.1. Request

GET '/add-album?target=album-id'

##### 1.6.0.2. Response

200 OK

### 1.7. users remove album from personal collection

##### 1.7.0.1. Request

GET '/remove-album?target=album-id'

##### 1.7.0.2. Response

200 OK

### 1.8. play a track

##### 1.8.0.1. Request

GET '/play&target=track-id'

##### 1.8.0.2. Response

200 OK

```http{.line-numbers}
Content-Type: multipart/form-data; boundary="boundary"

--boundary--

mp3 file

--boundary--

```
```json{.line-numbers}

{
    "name" : "xxx",
    "length" : "xxx",
    "lastPlay" : "xx:xx:xx"
}
```
```http{.line-numbers}
--boundary--

```


### 1.9. when a track is played, record the current time

##### 1.9.0.1. Request

GET '/track-lastplay?target=track-id&time=current-time'

##### 1.9.0.2. Response

200 OK

### 1.10. users upload new album

##### 1.10.0.1. Request

POST '/upload'

```http{.line-numbers}
Content-Type: multipart/form-data; boundary="boundary"

--boundary--

```
```json{.line-numbers}

{
    "name" : "xxx", 
    "artist" : "xxx",
    "tracks" : [
        "trackName1", "trackName2"
    ]
}
```
```http{.line-numbers}
--boundary--

mp3 file

--boundary--

mp3 file

--boundary

```


##### 1.10.0.2. Response

200 OK

### 1.11. users make comments on albums

POST '/comment?target=album-id'

```http{.line-numbers}
Content-Type: text

comments
```

### 1.12. users check album upload notification

##### 1.12.0.1. Request

GET '/check-upload-notification'

##### 1.12.0.2. Response

200 OK

```json{.line-numbers}
{
    "notification" : [
        {"albumName" : "xxx", "success" : "1/0"},
        {"albumName" : "xxx", "success" : "1/0"}
    ]
}
```


## 2. Admin

### 2.1. Admin login 

### 2.2. Admin search artists

### 2.3. Admin search albums

### 2.4. Admin add albums to personal collection

### 2.5. Admin remove albums to personal collection

### 2.6. Admin play a track 

### 2.7. when a track is played, record the current time

### 2.8. Admin make comments on albums

==All the above admin functions is the same as users==

### 2.9. Admin upload new albums to database

##### 2.9.0.1. Request

POST '/admin/upload'

header and body are the same as user upload albums

##### 2.9.0.2. Response

200 OK

### 2.10. Admin remove albums from database

##### 2.10.0.1. Request

GET 'admin/remove?target=album-id'

##### 2.10.0.2. Response

200 OK

### 2.11. Admin check user upload

##### 2.11.0.1. Request

GET 'admin/check-upload'

##### 2.11.0.2. Response

200 OK

```json{.line-numbers}
{
    "upload" : [
        {
            "userID" : "xxx",
            "userName" : "xxx",
            "album" : {
                "id" : "xxx",
                "name" : "xxx", 
                "artist" : "xxx",
                "tracks" : ["trackname1", "trackname2"]
            }
        }, 
        {
            "userID" : "xxx",
            "userName" : "xxx",
            "album" : {
                "id" : "xxx",
                "name" : "xxx", 
                "artist" : "xxx",
                "tracks" : ["trackname1", "trackname2"]
            }
        }
    ]
}
```


### 2.12. Admin reply user upload

##### 2.12.0.1. Request

POST 'admin/reply'

```json{.line-numbers}
{
    "reply" : [
        {
            "userID" : "xxx",
            "albumID" : "xxx"
        },
        {
            "userID" : "xxx",
            "albumID" : "xxx"
        }
    ]
}
```

##### 2.12.0.2. Response

200 OK

## 3. Database Schema Design

```sql{.line-numbers}
create table Album
(
    albumID varchar(10) NOT NULL,
    albumName varchar(50) NOT NULL,
    lastPlay time,
    primary key(albumID, trackID),
    foreign key(trackID) references Track(trackID)
);

create table Track
(
    trackID varchar(10) NOT NULL,
    trackName varchar(50) NOT NULL,
    trackLength int NOT NULL,
    lastPlay time,
    primary key(trackID)
);

create table Artist 
(
    artistID varchar(10) NOT NULL,
    artistName varchar(30) NOT NULL,
    albumID varchar(10) NOT NULL,
    primary key(artistID, albumID),
    foreign key(albumID) references Album(albumID)
);

create table User
(
    userID varchar(10) NOT NULL
    userName varchar(30) NOT NULL,
    Password varchar(30) NOT NULL,
    administrator boolean NOT NULL,
    primary key(userID) 
);

create table Comment
(
    userID varchar(10) NOT NULL,
    albumID varchar(10) NOT NULL,
    content varchar(200) NOT NULL,
    primary key(userID, albumID),
    foreign key(userID) references User(userID),
    foreign key(albumID) references Album(albumID)
);

create table Collect
(
    userID varchar(10) NOT NULL,
    albumID varchar(10) NOT NULL,
    primary key(userID, albumID),
    foreign key(userID) references User(userID),
    foreign key(albumID) references Album(albumID)
);

create table Upload
(
    userID varchar(10) NOT NULL,
    albumID varchar(10) NOT NULL,
    primary key(userID, albumID),
    foreign key(userID) references User(userID),
    foreign key(albumID) references Album(albumID)
);













