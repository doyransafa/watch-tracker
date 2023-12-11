
# Django/htmx - Watch Tracker with TMDB API

## Features

- Login/Logout/Register
- Active search for Movies, TV Shows and People.
- Movie and TV Series details pages.
- Interact with Movie/TV Series by marking watched, like, bookmark or add comment.
- Rate or interact with individual episodes and seasons.
- Create public, private or friends only lists.
- Follow other users, see their interactions on your feed.
- Display users liked, watched, rated collections.


## Video Demo
### [Demo Video Link](https://drive.google.com/file/d/10HyCOCk8ZOyzkELMJtfKsof7TTHGLkzk/view)

<img width="721" alt="image" src="https://github.com/doyransafa/watch-tracker/assets/72417108/0ec6bb4d-1814-435b-956b-8131bfe9161a">

## Build Steps

Create a virtual environment

    python -m venv /path/to/new/virtual/environment

Activate virtual environment  
MacOS:

    source venv/bin/activate

for Windows PowerShell

    <venv_path>\Scripts\Activate.ps1  

Install dependencies 

    pip install -r requirements.txt

Migrate database  

    python manage.py makemigrations
    python manage.py migrate

Create admin user. Needed if you want to use Admin dashboard.

    python manage.py createsuperuser

Start server, port number is optional, default is 8000

    python manage.py runserver 8080
