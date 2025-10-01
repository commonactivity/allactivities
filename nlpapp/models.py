from django.db import models
from django.contrib.auth.models import User

# Uploads of PDF/TXT files
class Upload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    wordcloud = models.ImageField(upload_to='wordclouds/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} by {self.user.username}"


# Optional: Track sessions per user for activity
class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_name = models.CharField(max_length=255)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.session_name} ({self.user.username})"


# Optional: Store WordCloud history
class WordCloudHistory(models.Model):
    upload = models.ForeignKey(Upload, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='wordclouds/')

    def __str__(self):
        return f"WordCloud for {self.upload.file.name}"
