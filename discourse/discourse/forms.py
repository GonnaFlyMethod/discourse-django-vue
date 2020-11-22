from django import forms
from .models import Comment
from ckeditor.widgets import CKEditorWidget


class RichEditorForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget(attrs={'id':
    	                                                'text_comment__'}))
    class Meta:
        model = Comment
        fields = ['text',]