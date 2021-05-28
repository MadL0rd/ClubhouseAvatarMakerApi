# ClubhouseAvatarMakerApi

API for ClubhouseAvatarMaker mobile client.

## Installation

- Download ClubhouseAvatarMakerApi zip or clone
- Create file with name ```.env.uu``` and put into login and password in this format
```
POSTGRES_USER=YourSuperUsername
POSTGRES_PASS=YourSuperPassword
```
- Then run this commands from project root directory
``` bash
docker exec -it cl_django python manage.py migrate
docker exec -it cl_django python manage.py createsuperuser
docker exec -it cl_django python manage.py collectstatic
```

## Api routes information

### Current endpoint 
http://80.78.247.50/api/

## Routes:

- <strong> Get borders </strong>

Return borders with pagination

Parameters: page
```
GET endpoint/api/borders/?page=1
```


- <strong> Get token </strong>

Token needs to take user possibility to use codes and provide user custom access to borders

```
GET endpoint/api/get_token/
```

Use next authorization headers to get access to other
```
"Authorization": "Token UserToken"
```

- <strong> Get used codes (require authorization) </strong>
```
GET endpoint/api/codes/
```


- <strong> Use code (require authorization) </strong>
Parameters: code
```
POST endpoint/api/codes/?code=code2use
```


- <strong> Get branded borders (require authorization) </strong>
```
GET endpoint/api/borders_new/
```


## License

ClubhouseAvatarMakerApi is licensed under the terms of the [Apache License, version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html). Please see the [LICENSE](LICENSE) file for full details.
