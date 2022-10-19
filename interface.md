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

if user-name is repeated:

400 Bad Request

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

set-cookie: session = xxx

if login fail (e.g. wrong password)

403 forbidden

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

if not in login status: 

403 forbidden

### 1.4. given album id, get album information (not for user)

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

if not in login status:

403 forbidden

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

if not in login status:

403 forbidden

### 1.6. users add album to personal collection

##### 1.6.0.1. Request

POST '/add-album?target=album-id'

##### 1.6.0.2. Response

200 OK

if not in login status:

403 forbidden

### 1.7. users remove album from personal collection

##### 1.7.0.1. Request

POST '/remove-album?target=album-id'

##### 1.7.0.2. Response

200 OK

if not in login status:

403 forbidden

### 1.8. play a track

##### 1.8.0.1. Request

GET '/play?target=track-id'

##### 1.8.0.2. Response

200 OK

```json{.line-numbers}

{
    "name" : "xxx",
    "length" : "xxx",
    "lastPlay" : "xx:xx:xx",
    "url" : "xx"
}
```

if not in login status:

403 forbidden

### 1.9. when a track is played, record the current time

##### 1.9.0.1. Request

POST '/track-lastplay?target=track-id&time=current-time'

##### 1.9.0.2. Response

200 OK

### 1.10. users upload new album

##### 1.10.0.1. Request

POST '/upload'

```http{.line-numbers}
Content-Type: multipart/form-data; boundary="boundary"

--boundary--

```

use XMLHttpRequest FormData

```javascript{.line-numbers}
var formData = new FormData()
formData.append("name", "xxx")
formData.append("artist", "xxx")
formData.append("trackName1", file)
formData.append("trackName1", file)

```

##### 1.10.0.2. Response

200 OK

if not in login status: 

403 forbidden

### 1.11. users make comments on albums

##### 1.11.0.1 Request

POST '/comment?target=album-id'

```http{.line-numbers}
Content-Type: text

comments
```

##### 1.11.0.2 Response

200 OK

if not in login status:

403 forbidden

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

if not in login status:

403 forbidden


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

if not in login status: 

403 forbidden

### 2.10. Admin remove albums from database

##### 2.10.0.1. Request

POST 'admin/remove?target=album-id'

##### 2.10.0.2. Response

200 OK

if not in login status: 

403 forbidden

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
                "tracks" : [
                    {"trackID" : "xxx", "trackName" : "xxx"},
                    {"trackID" : "xxx", "trackName" : "xxx"}
                    ]
            }
        }, 
        {
            "userID" : "xxx",
            "userName" : "xxx",
            "album" : {
                "id" : "xxx",
                "name" : "xxx", 
                "artist" : "xxx",
                "tracks" : [
                    {"trackID" : "xxx", "trackName" : "xxx"},
                    {"trackID" : "xxx", "trackName" : "xxx"}
                    ]
            }
        }
    ]
}
```

if not in login status: 

403 forbidden

### 2.12. Admin reply user upload

##### 2.12.0.1. Request

POST 'admin/reply'

```json{.line-numbers}
{
    "reply" : [
        {
            "userID" : "xxx",
            "albumID" : "xxx",
            "success" : "1/0"
        },
        {
            "userID" : "xxx",
            "albumID" : "xxx",
            "success" : "1/0"
        }
    ]
}
```

##### 2.12.0.2. Response

200 OK

if not in login status: 

403 forbidden

## 3. Database Schema Design

```sql{.line-numbers}
create table Album
(
    albumID varchar(10) NOT NULL,
    albumName varchar(50) NOT NULL,
    lastPlay time,
    primary key(albumID),
    foreign key(artistID) references Artist(artistID)
);

create table Track
(
    trackID varchar(10) NOT NULL,
    trackName varchar(50) NOT NULL,
    trackLength time NOT NULL,
    trackIndex int NOT NULL,
    lastPlay time,
    primary key(trackID),
    foreign key(albumID) references Album(albumID) ON DELETE CASCADE
);

create table Artist 
(
    artistID varchar(10) NOT NULL,
    artistName varchar(30) NOT NULL,
    primary key(artistID),
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
    foreign key(albumID) references Album(albumID) ON DELETE CASCADE
);

create table Collect
(
    userID varchar(10) NOT NULL,
    albumID varchar(10) NOT NULL,
    primary key(userID, albumID),
    foreign key(userID) references User(userID),
    foreign key(albumID) references Album(albumID) ON DELETE CASCADE
);

create table Upload
(
    userID varchar(10) NOT NULL,
    albumID varchar(10) NOT NULL, // 临时分配
    albumName varchar(50) NOT NULL,
    trackID varchar(10) NOT NULL,
    trackName varchar(50) NOT NULL,
    artistName varchar(30) NOT NULL,
    granted boolean NOT NULL,
    primary key(userID, albumID, trackID),
    foreign key(userID) references User(userID),
);
```