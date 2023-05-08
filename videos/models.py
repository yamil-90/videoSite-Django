from typing import Type
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator, ValidationError
from PIL import Image
from django.db.models.options import Options

def validate_video_size(value):
    filesize = value.size

    if filesize > 10485760:
        raise ValidationError("The maximum file size that can be uploaded is 10MB")


# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField()

    video_file = models.FileField(upload_to='assets/videos/', validators=[FileExtensionValidator(allowed_extensions=['mp4']), validate_video_size])
    thumbnail = models.ImageField(upload_to='assets/thumbnails/')

    categories = models.ManyToManyField('Category', related_name='videos')
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.video_file and not self.thumbnail:
            # Open the video file using Pillow
            with Image.open(self.video_file.path) as video:
                # Generate a thumbnail by resizing the video
                video.thumbnail((300, 300))
                # Save the thumbnail to the database
                self.thumbnail.save(f'{self.title}.png', video.format, save=False)
                # Update the video model instance
                self.save(update_fields=['thumbnail'])

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField()
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.video.title} - {self.text[:50]}"
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()



    def __str__(self):
        return self.name