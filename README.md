# General description
django_google_drive_api is a django project, created for uploading files to Google Drive, 
by passing the file's name and the file's text content. \
Main stack and tools: Django, Djangorestframework, Postgresql, Nginx, Gunicorn, google-api-python-client, google-auth, 
google-auth-httplib2.

# Usage
1. The project is deployed on the server with IP 158.160.72.208
   - Go to http://158.160.72.208/docs/ and create files with the swagger interface.
   - Go to http://158.160.72.208/drive_api/upload/ and create files with the drf interface.

2. Access the project's documentation:
   - http://158.160.72.208/docs/

# Testing
-All the endpoints are covered by pytest tests in /tests/test_main.py \
- Run tests:\
  docker-compose exec app_sales_networks python manage.py test

