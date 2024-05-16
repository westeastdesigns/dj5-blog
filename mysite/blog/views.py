from django.shortcuts import get_object_or_404, render
from .models import Post
from django.http import Http404


def post_detail(request, id):
    """post_detail view for a single post

    Args:
        request (object): required by all views
        id (int): id argument of a post

    Raises:
        Http404: if no object is found

    Returns:
        url: detail.html blog post detail view template
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

def post_list(request):
    """post_list _summary_

    Args:
        request (object): required by all views

    Returns:
        url: list.html render the list of posts with the given template
    """
    posts = Post.published.all()
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )

