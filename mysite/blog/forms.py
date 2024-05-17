from django import forms

# blog/forms.py defines forms used by the blog application


class EmailPostForm(forms.Form):
    """EmailPostForm defines the form to recommend posts via email.
    EmailPostForm inherits from the base Form class and validates form data according to its field type.

    Args:
        forms (CharField) name: name of person sending the post
        forms (EmailField) email: email of person sending the post recommendation
        forms (EmailField) to: email of recipient
        forms (CharField) comments: optional field for comments to include in the email with widget
    """

    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
