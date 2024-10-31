This is a Django-based API project for an article "like" feature. The API allows users to register, log in, view articles, and "like" individual articles.
Each article displays its current like count.

- User registration and login with token-based authentication.
- Create, view, update, and delete articles.
- Like an article, with unique likes per user.
- Swagger-based API documentation.
- TinyMCE integration for article content editing.


Install Dependencies
pip install -r requirements.txt

Set up a MySQL database and update the DATABASES setting in your Django settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

Run Migrations
python manage.py migrate

Create a Superuser
python manage.py createsuperuser

Start the Server
python manage.py runserver

Access Admin Interface
Go to http://127.0.0.1:8000/admin/ and log in with your superuser credentials.

API Documentation
Swagger UI is available for testing and viewing API endpoints. Once the server is running, access Swagger UI at:
http://127.0.0.1:8000/swagger/
