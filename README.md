# NLP Project
Django-based NLP app with:
- PDF/TXT upload
- Wordcloud generation
- User activity history
- Admin dashboard with charts

Run:
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
