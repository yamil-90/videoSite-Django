from django import forms
from django.core.validators import FileExtensionValidator
from .helpers import validate_video_size
from .models import Category

    
class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3,  strip=True, 
                              widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a public comment...', 'rows': 1}))
    

class VideoCreateForm(forms.Form):
    title = forms.CharField(required=True, max_length=255, min_length=3, strip=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'})
                            )

    description = forms.CharField(required=True, max_length=500, min_length=3, strip=True, 
                                  widget=forms.Textarea(attrs={'class': 'form-control'}))

    video_file = forms.FileField(required=True, 
                                 validators=[FileExtensionValidator(allowed_extensions=['mp4']), 
                                             validate_video_size],
                                             widget=forms.FileInput(attrs={'class': 'form-control'})
                                             )

    thumbnail = forms.ImageField(required=True,
                                 widget=forms.FileInput(attrs={'class': 'form-control'})
                                    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        label="Categories",
        required=False,
    )
# https://docs.djangoproject.com/en/3.0/topics/http/file-uploads/
# https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
# https://stackoverflow.com/questions/32007311/how-to-change-data-in-django-modelform
# https://docs.djangoproject.com/en/3.0/ref/forms/validation/#cleaning-and-validating-fields-that-depend-on-each-other