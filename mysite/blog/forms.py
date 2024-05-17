from django import forms

from .models import Comment

# blog/forms.py defines forms used by the blog application


class EmailPostForm(forms.Form):
    """EmailPostForm defines the form to recommend posts via email.
    EmailPostForm inherits from the base Form class and validates form data according to its field type.

    Args:
        name (CharField): name of person sending the post
        email (EmailField): email of person sending the post recommendation
        to (EmailField): email of recipient
        comments (CharField): optional field for comments to include in the email with widget
    """

    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    """CommentForm provides a form for users to input comments on posts.

    Args:
        forms (model form): using the Comment model
        fields (string tuple): the fields to include in the comment form
    """

    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
