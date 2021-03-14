## Audio File Server API

## Setting up the virtual env and install dependencies
Go inside the project folder and execute the below commands.

```
sudo pip install virtualenv 
virtualenv venv 
source venv/bin/activate
pip install -r requirements.txt
```
Dependencies will be installed from the requirements.txt. Python version 3.7 is used for this project.

## Run the Application

```
FLASK_APP=wsgi.py FLASK_ENV=development flask run
```

This will start the application on port 5000

## Test the application

Swagger-UI can be used to test the application.

<img width="919" alt="Screen Shot" src="https://user-images.githubusercontent.com/17323570/111064077-5892e880-84b2-11eb-9b62-aeba9a32c051.png">


The server will start at <http://localhost:5000>.

**audioFileMetadata** for creating a **song**
```
{
  "name": "Michael",
  "duration": 305
}
```

**audioFileMetadata** for creating a **podcast**
```
{
  "name": "Michael's Podcast",
  "host": "Michael",
  "duration": 800,
  "participants": ["Michael Owen", "Michael Jordan", "Michael Ballack"]
}
```

**audioFileMetadata** for creating an **audiobook**
```
{
  "title": "Michael",
  "author": "Michael",
  "narrator": "Michael Douglas",
  "duration": 900,
}
```
