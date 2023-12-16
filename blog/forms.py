from django import forms
from django.forms import widgets
from .models import Comment

class SearchForm(forms.Form):
    pass
    query = forms.CharField()


class CommentForm(forms.ModelForm):
    parent_comment = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }