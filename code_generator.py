import os

# ----- CONFIG -----
PROJECT_NAME = "nlp_project"
APP_NAME = "nlpapp"

BASE_DIR = os.getcwd()
PROJECT_DIR = os.path.join(BASE_DIR, PROJECT_NAME)
APP_DIR = os.path.join(BASE_DIR, APP_NAME)

TEMPLATES_DIR = os.path.join(APP_DIR, "templates", APP_NAME)
STATIC_DIR = os.path.join(APP_DIR, "static", APP_NAME)
CSS_DIR = os.path.join(STATIC_DIR, "css")
JS_DIR = os.path.join(STATIC_DIR, "js")

# ----- HELPER -----
def create_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Created: {path}")
    else:
        print(f"⚠️ Exists, skipping: {path}")

# ----- ROOT FILES -----
manage_py = """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{PROJECT_NAME}.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django not installed") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""".format(PROJECT_NAME=PROJECT_NAME)

requirements_txt = """Django>=4.2
matplotlib
wordcloud
nltk
pdfplumber
Pillow
"""

readme_md = """# NLP Project
Django-based NLP app with:
- PDF/TXT upload
- Wordcloud generation
- User activity history
- Admin dashboard with charts

Run:
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
"""

create_file(os.path.join(BASE_DIR, "manage.py"), manage_py)
create_file(os.path.join(BASE_DIR, "requirements.txt"), requirements_txt)
create_file(os.path.join(BASE_DIR, "README.md"), readme_md)

# ----- PROJECT FILES -----
project_files = {
    "__init__.py": "",
    "settings.py": """import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'replace-this-with-a-secret-key'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '{APP_NAME}',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{PROJECT_NAME}.urls'

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

WSGI_APPLICATION = '{PROJECT_NAME}.wsgi.application'
ASGI_APPLICATION = '{PROJECT_NAME}.asgi.application'

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
""".format(PROJECT_NAME=PROJECT_NAME, APP_NAME=APP_NAME),
    "urls.py": """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('{APP_NAME}.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
""".format(APP_NAME=APP_NAME),
    "wsgi.py": """import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{PROJECT_NAME}.settings')
application = get_wsgi_application()
""".format(PROJECT_NAME=PROJECT_NAME),
    "asgi.py": """import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '{PROJECT_NAME}.settings')
application = get_asgi_application()
""".format(PROJECT_NAME=PROJECT_NAME),
}

for filename, content in project_files.items():
    create_file(os.path.join(PROJECT_DIR, filename), content)

# ----- APP FILES -----
app_files = {
    "__init__.py": "",
    "views.py": """from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, '{APP_NAME}/dashboard.html')

@login_required
def history(request):
    return render(request, '{APP_NAME}/history.html')
""".format(APP_NAME=APP_NAME),
    "models.py": """from django.db import models
from django.contrib.auth.models import User

class Upload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    wordcloud = models.ImageField(upload_to='wordclouds/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
""",
    "forms.py": """from django import forms
from .models import Upload

class UploadForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['file']
""",
    "urls.py": """from django.urls import path
from . import views

app_name = '{APP_NAME}'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('history/', views.history, name='history'),
]
""".format(APP_NAME=APP_NAME),
    "admin.py": """from django.contrib import admin
from .models import Upload

@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = ('user', 'file', 'created_at')
"""
}

for filename, content in app_files.items():
    create_file(os.path.join(APP_DIR, filename), content)

# ----- TEMPLATES -----
os.makedirs(TEMPLATES_DIR, exist_ok=True)
templates = {
    "base.html": """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{% block title %}NLP App{% endblock %}</title>
<link rel="stylesheet" href="{% static 'nlpapp/css/style.css' %}">
</head>
<body>
{% block content %}{% endblock %}
</body>
</html>
""",
    "dashboard.html": """{% extends 'nlpapp/base.html' %}
{% block content %}
<h2>Dashboard</h2>
{% endblock %}""",
    "history.html": """{% extends 'nlpapp/base.html' %}
{% block content %}
<h2>History</h2>
{% endblock %}""",
    "admin_dashboard.html": """{% extends 'nlpapp/base.html' %}
{% block content %}
<h2>Admin Dashboard</h2>
{% endblock %}""",
}

for name, content in templates.items():
    create_file(os.path.join(TEMPLATES_DIR, name), content)

# ----- STATIC FILES -----
os.makedirs(CSS_DIR, exist_ok=True)
os.makedirs(JS_DIR, exist_ok=True)

create_file(os.path.join(CSS_DIR, "style.css"), "body { font-family: Arial; }")
create_file(os.path.join(JS_DIR, "main.js"), "console.log('JS loaded');")

# ----- AUTH TEMPLATES -----
auth_templates = {
    "login.html": """{% extends 'nlpapp/base.html' %}
{% block title %}Login{% endblock %}
{% block content %}
<h2>Login</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn btn-primary" type="submit">Login</button>
</form>
<p>Don't have an account? <a href="{% url 'signup' %}">Sign up here</a>.</p>
{% endblock %}""",

    "signup.html": """{% extends 'nlpapp/base.html' %}
{% block title %}Signup{% endblock %}
{% block content %}
<h2>Sign Up</h2>
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button class="btn btn-success" type="submit">Register</button>
</form>
<p>Already have an account? <a href="{% url 'login' %}">Login here</a>.</p>
{% endblock %}""",

    "logout.html": """{% extends 'nlpapp/base.html' %}
{% block title %}Logged Out{% endblock %}
{% block content %}
<h2>You have been logged out.</h2>
<a href="{% url 'login' %}" class="btn btn-primary">Login again</a>
{% endblock %}""",
}

for name, content in auth_templates.items():
    create_file(os.path.join(TEMPLATES_DIR, name), content)
