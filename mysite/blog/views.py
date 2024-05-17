from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render

from .models import Post


def post_list(request):
    """post_list paginates and displays the list of all posts.
    paginator assigned by Paginator class returns 3 posts from post_list per page.
    page_number variable stores the page GET HTTP parameter, page 1 loads by default.
    posts variable stores objects from the chosen Page object from the page() method.

    Args:
        request (object): required by all views

    Returns:
        url (list.html): renders the list of posts with the given template
    """
    post_list = Post.published.all()
    # Paginates with three posts per page
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # if page_number is not an integer, get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # if page_number is out of range, get last page of results
        posts = paginator.page(paginator.num_pages)
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    """post_detail displays a single post. Uses the get_object_or_404 shortcut.

    Args:
        request (object): required by all views
        view takes these arguments of a post to identify which post to show:
        slug (string): unique slug identifying post
        year (int): year post was published
        month (int): month post was published
        day (int): day post was published

    Raises:
        Http404: if no object is found

    Returns:
        url (detail.html): renders the blog post detail view template
    """
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(request, "blog/post/detail.html", {"post": post})
