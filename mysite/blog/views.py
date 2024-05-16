from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):
    """post_list displays the list of posts

    Args:
        request (object): required by all views

    Returns:
        url (list.html): renders the list of posts with the given template
    """
    posts = Post.published.all()
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def post_detail(request, id):
    """post_detail displays a single post. Uses the get_object_or_404 shortcut.

    Args:
        request (object): required by all views
        id (int): this view takes the id argument of a post to identify which post to show

    Raises:
        Http404: if no object is found

    Returns:
        url (detail.html): renders the blog post detail view template
    """
    post = get_object_or_404(
        Post,
        id=id,
        status=Post.Status.PUBLISHED
    )
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )
