from django import forms
from .models import Post,Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PostCreationForm(forms.ModelForm):
    title = forms.CharField(widget = forms.Textarea)
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = [
        'title', 'content'
        ]

class PostUpdateForm(forms.ModelForm):
    title = forms.CharField(widget = forms.Textarea)
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = [
        'title', 'content'
        ]

class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
        'comment'
        ]
