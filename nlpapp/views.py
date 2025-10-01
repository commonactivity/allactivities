from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadForm
from django.contrib.admin.views.decorators import staff_member_required
import matplotlib
matplotlib.use('Agg')
import matplotlib as plt 
import io
import base64
from .models import Upload, UserSession, WordCloudHistory
from wordcloud import WordCloud
import os
from .models import Upload
from django.conf import settings
import pdfplumber
import nltk
from django.contrib.auth.forms import UserCreationForm

nltk.download('stopwords')
from nltk.corpus import stopwords
import string
stop_words = set(stopwords.words('french'))

@staff_member_required
def admin_dashboard(request):
    """
    Custom admin dashboard showing charts
    """
    #Example: Number of uploads per user
    from django.contrin.auth.models import user
    users = user.objects.all()
    upload_counts = [Upload.objects.filter(user=u).count() for u in users]
    userlabels = [u.username for u in users]
    #bar chart
    plt.figure(figsize=(8,4))
    plt.bar(user_labels,upload_counts,color='skyblue')
    plt.xlabel('Users')
    plt.ylabel("Number of uploads")
    plt.title("Uploads per user")
    plt.tight_layout()

    #Convert chart to PNG image
    buf = io.bytesIO()
    plt.savefig(buf,format='png')
    buf.seek(0)
    chart_base64 = base64.b64encode(bu.read()).decode('utf-8')
    plt.close()
    #Total wordcloud generated
    total_wc = WordCloudHistory.objects.count()
    return render(request,'nlpapp/admin_dashboard.html',{'chart_base64':chart_base64,'total_uploads':Upload.objects.count(),'total_wordclouds':total_wc})

@login_required
def dashboard(request):
    # Start a new session if needed
    session, created = UserSession.objects.get_or_create(
        user=request.user,
        session_name=f"Session {request.user.id}-{UserSession.objects.filter(user=request.user).count()+1}",
        finished_at=None
    )

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_obj = form.save(commit=False)
            upload_obj.user = request.user
            upload_obj.save()

            # Extract text
            file_path = os.path.join(settings.MEDIA_ROOT, upload_obj.file.name)
            text = ""
            if upload_obj.file.name.lower().endswith('.pdf'):
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
            #Remove punctuations
            text = re.sub(r'[^\w\s]',text)
            #Remove stopwords
            words = text.split()
            filtered_words = [w for w in words if w.lower() not in stopwords and w not in string.punctuation]
            filtered_text = ''.join(filtered_words)
            print(filtered_text)
            # Generate WordCloud
            
            wc = WordCloud(width=800, height=400, background_color='white').generate(filtered_text)
            wc_path = os.path.join(settings.MEDIA_ROOT, 'wordclouds', f'wc_{upload_obj.id}.png')
            os.makedirs(os.path.dirname(wc_path), exist_ok=True)
            wc.to_file(wc_path)
            upload_obj.wordcloud = f'wordclouds/wc_{upload_obj.id}.png'
            upload_obj.save()

            

            # Save in WordCloudHistory
            WordCloudHistory.objects.create(upload=upload_obj, image=upload_obj.wordcloud)

            return redirect('nlpapp:history')
    else:
        form = UploadForm()

    uploads = Upload.objects.filter(user=request.user)
    sessions = UserSession.objects.filter(user=request.user)
    return render(request, 'nlpapp/dashboard.html', {
        'form': form,
        'uploads': uploads,
        'sessions': sessions
    })



@login_required
def history(request):
    """
    Display all uploads and WordClouds for the current user.
    """
    uploads = Upload.objects.filter(user=request.user)
    return render(request, 'nlpapp/history.html', {'uploads': uploads})



def signup(request):
    """
    User registration view
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('nlpapp:login')
    else:
        form = UserCreationForm()
    return render(request, 'nlpapp/signup.html', {'form': form})


@login_required
def upload_file(request):
    """
    Handle file upload and WordCloud generation
    """
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            upload_obj = form.save(commit=False)
            upload_obj.user = request.user
            upload_obj.save()

            # Extract text
            file_path = os.path.join(settings.MEDIA_ROOT, upload_obj.file.name)
            text = ""
            if upload_obj.file.name.lower().endswith('.pdf'):
                with pdfplumber.open(file_path) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text() + "\n"
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()

            # Generate WordCloud
            wc = WordCloud(width=800, height=400, background_color='white').generate(text)
            wc_path = os.path.join(settings.MEDIA_ROOT, 'wordclouds', f'wc_{upload_obj.id}.png')
            os.makedirs(os.path.dirname(wc_path), exist_ok=True)
            wc.to_file(wc_path)
            upload_obj.wordcloud = f'wordclouds/wc_{upload_obj.id}.png'
            upload_obj.save()

            # Save to WordCloudHistory
            WordCloudHistory.objects.create(upload=upload_obj, image=upload_obj.wordcloud)

            return redirect('nlpapp:history')
    else:
        form = UploadForm()

    return render(request, 'nlpapp/upload.html', {'form': form})
