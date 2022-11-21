[toc]
## 1. Users

### 1.1. users register

##### 1.1.0.1. Request

提交注册信息:

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

提交登陆信息

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

```json
{
    "isAdmin": True / False
}
```

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

GET 'search-album-id?target=album-id'

GET 'search-album-id/'

##### 1.4.0.2. Response

```json
{
    "albums": [
        {
            "id" : "xxx",
            "name" : "xxx",
            "artist" : "xxx",
            "tracks" : [
                {"trackID" : "xxx", "trackName" : "xxx"},
                {"trackID" : "xxx", "trackName" : "xxx"}
            ],
            "comments": [
                {"userID": "xxx", "comment": "xxx"},
                {"userID": "xxx", "comment": "xxx"}
            ]
        },
        ......
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

允许同名album存在, 所以可能返回多个albums

```json{.line-numbers}
{
    "albums": [
        {
            "id" : "xxx",
            "name" : "xxx",
            "artist" : "xxx",
        },
        {
            "id" : "xxx",
            "name" : "xxx",
            "artist" : "xxx",
        },
    ]
}
```

if not in login status:

403 forbidden

### User check person collection

#### Request

GET 'check-collection/'

#### Response

200 OK

```json
{
    "albums": [
        {
            "id" : "xxx",
            "name" : "xxx",
            "artist" : "xxx",
            "tracks" : [
                {"trackID" : "xxx", "trackName" : "xxx"},
                {"trackID" : "xxx", "trackName" : "xxx"}
            ],
            "comments": [
                {"userID": "xxx", "comment": "xxx"},
                {"userID": "xxx", "comment": "xxx"}
            ]
        },
        ......
    ]
}
```

if not in login status:

403 forbidden

### 1.6. users add album to personal collection

##### 1.6.0.1. Request

POST '/add-album'

```json
{
    "id" : "xxx"
}
```

##### 1.6.0.2. Response

200 OK

if not in login status:

403 forbidden

### 1.7. users remove album from personal collection

##### 1.7.0.1. Request

POST '/remove-album'

```json
{
    "id": "xxx"
}
```

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
    "length" : length, // measured in seconds
    "lastPlay" : unix timestamp in integer,
    // if no lastplay info, it will be set to -1
    "url" : "xx"
}
```

if not in login status:

403 forbidden

### 1.9. when a track is played, record the current time

##### 1.9.0.1. Request

POST '/track-lastplay'

```json
{
    "id": "xxx",
    "time": "xxx"
}
```

time is expressed in unix timestamp

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

POST '/comment'

```json{.line-numbers}
{
    "id": "xxx",
    "comment": "xxxxxxxxx"
}
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
        {"albumName" : "xxx", "status" : "success/fail/waiting"},
        {"albumName" : "xxx", "status" : "success/fail/waiting"}
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

POST 'admin/remove'

```json
{
    "id": "xxx"
}
```

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
            "albumID" : "xxx",
            "success" : "1/-1" // 1 represent success, -1 represent fail
        },
        {
            "albumID" : "xxx",
            "success" : "1/-1"
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
    albumID TEXT NOT NULL,
    albumName TEXT NOT NULL,
    lastPlay INTEGER, // unix timestamp
    uploaderID TEXT,
    granted INTEGER NOT NULL,
    primary key(albumID),
    foreign key(artistID) references Artist(artistID)
);

create table Track
(
    trackID TEXT NOT NULL,
    trackName TEXT NOT NULL,
    trackLength REAL NOT NULL, // measured in seconds
    trackIndex INTEGER NOT NULL,
    lastPlay INTEGER, // unix timestamp
    primary key(trackID),
    foreign key(albumID) references Album(albumID) ON DELETE CASCADE
);

create table Artist 
(
    artistID TEXT NOT NULL,
    artistName TEXT NOT NULL,
    primary key(artistID),
);

create table User
(
    userID TEXT NOT NULL
    userName TEXT NOT NULL,
    -- Password TEXT NOT NULL,
    -- administrator boolean NOT NULL, 使用django内置user model
    primary key(userID) 
);

create table Comment
(
    userID TEXT NOT NULL,
    albumID TEXT NOT NULL,
    content TEXT NOT NULL,
    primary key(userID, albumID),
    foreign key(userID) references User(userID),
    foreign key(albumID) references Album(albumID) ON DELETE CASCADE
);

create table Collect
(
    userID TEXT NOT NULL,
    albumID TEXT NOT NULL,
    primary key(userID, albumID),
    foreign key(userID) references User(userID),
    foreign key(albumID) references Album(albumID) ON DELETE CASCADE
);


-- do not create new table for relation upload, merge this relation to table album
-- create table Upload
-- (
--     userID varchar(10) NOT NULL,
--     albumID varchar(10) NOT NULL, // 临时分配
--     albumName varchar(50) NOT NULL,
--     trackID varchar(10) NOT NULL,
--     trackName varchar(50) NOT NULL,
--     trackIndex INTEGER NOT NULL,
--     artistName varchar(30) NOT NULL,
--     granted INTEGER NOT NULL, // 0 未处理, 1 允许, -1 拒绝
--     primary key(userID, albumID, trackID),
--     foreign key(userID) references User(userID),
-- );
```
