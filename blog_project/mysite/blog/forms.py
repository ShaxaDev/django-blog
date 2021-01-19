from django import forms
from blog.models import Post,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=('title','content')
        widgets={
            'title':forms.TextInput(attrs={'class':'textinputclass'}),
            'content':forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'})
        }
    
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=('text',)

        widgets={
            
            'text':forms.Textarea(attrs={'class':'editable medium-editor-textarea'})
        }