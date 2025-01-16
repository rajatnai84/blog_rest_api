# Blog API

## Tech Stack

<p>
    <img alt="Python" src="https://img.shields.io/badge/-Python-9c7200?style=flat-square&logo=python&logoColor=white" />
    <img alt="pip" src="https://img.shields.io/badge/-pip-003585?style=flat-square&logo=pypi&logoColor=white" />
    <img alt="django" src="https://img.shields.io/badge/django-0b5200?style=flat-square&logo=django&logoColor=white" />
    <img alt="postgres" src="https://img.shields.io/badge/prisma-purple?style=flat-square&logo=postgresql&logoColor=white" />
</p>

REST api which provides backend routes for the authentication & authorization with JWT (access and refresh tokens), blog CRUD operations, filter, search and pagination for the blogs retrieval quires and comments functionality, also had email notification.

Other than that using [django-silk](https://github.com/jazzband/django-silk) for inspection of database quires and HTTP requests. Using [drf-spectacular](https://github.com/tfranzel/drf-spectacular) which is using OpenAi 3 model for schema and documentation generation tool by using it application is providing the swagger-ui.

## Local Setup

1. Cloning repo

```
git clone https://github.com/rajatnai84/blog_rest_api
cd blog_rest_api
```

2. Set virtual env
   
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Set .env
   
4. Install dependencies 
   
```bash
pip install -r requirements.txt
```

5. Run project

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

#### If Postgres connection 

   
1. Create the database locally

```sql
CREATE DATABASE <give-db-name>;
```

2. Change .env change in settings.py

```bash
DATABASE_URL=<new>
```

## Testing

Go to this route `http://127.0.0.1:8000/api/schema/swagger-ui/` in browser, would show the swagger-documentation and api routes.