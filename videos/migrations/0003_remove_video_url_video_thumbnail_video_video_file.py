# Generated by Django 4.0.7 on 2023-05-06 20:57

import django.core.validators
from django.db import migrations, models
import videos.models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_video_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='url',
        ),
        migrations.AddField(
            model_name='video',
            name='thumbnail',
            field=models.ImageField(default='error', upload_to='thumbnails/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='video_file',
            field=models.FileField(default='error', upload_to='videos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4']), videos.models.validate_video_size]),
            preserve_default=False,
        ),
    ]
