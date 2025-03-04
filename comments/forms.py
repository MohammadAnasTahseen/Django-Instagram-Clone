from django import forms
from comments.models import Comment


class PostCommentsForm(forms.ModelForm):
    
    

    body = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Enter your comment'}), required=True)


    class Meta:
        model = Comment
        fields = ['body']






