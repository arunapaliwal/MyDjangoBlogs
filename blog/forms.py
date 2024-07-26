from django import forms
from .models import Comment,Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ["post"]
        labels = {
            "user_name":"Your Name",
            "user_email":"Your Email",
            "text":"Comment",
        }


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ["slug"]
        labels = {
            "title":"Post Title",
            "excerpt":"Quote",
            "image":"Post Image",
        }
