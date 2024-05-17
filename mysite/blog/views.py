from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .forms import CommentForm, EmailPostForm
from .models import Post


def post_list(request):
    """post_list function-based view paginates and displays the list of all posts.
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
    # adds a QuerySet to retrieve a list of active comments for this post
    comments = post.comments.filter(active=True)
    # creates an instance of the comment form for users to comment
    form = CommentForm()

    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


class PostListView(ListView):
    """PostListView class-based view paginates and displays the list of all posts.
    Inherits from ListView.

    Args:
        ListView (generic class): allows any type of object to be listed
    """

    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_share(request, post_id):
    """post_share function-based view creates an instance of the post sharing form and
    handles form submission. post_share utilizes the get_object_or_404() shortcut to
    retrieve as published post by its id. On load, the view receives a GET request. On
    submission, the view receives a POST request and validates it. Validated data is
    retrieved with form.cleaned_data attribute, a dict of form fields and their values.

    Args:
        request (object): the request
        post_id (integer): identifies the post being referenced

    Returns:
        share.html (string): url where form data rendered to html page
        form, post (dict): validated post and form data rendered to dictionary
    """
    post = get_object_or_404(
        # retrieve post by id
        Post,
        id=post_id,
        status=Post.Status.PUBLISHED,
    )
    sent = False

    if request.method == "POST":
        # form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # if form fields passed validation, data is clean
            cd = form.cleaned_data
            # then send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = (
                f"{cd['name']} ({cd['email']}) " f"recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd["to"]],
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )


@require_POST
def post_comment(request, post_id):
    """post_comment function-based view processes the form and allows the user to
    return to the post detail once the comment is stored in the database.

    Args:
        request (object): the request
        post_id (integer): identifies the post being referenced

    Returns:
        comment.html (string): url where form data rendered to html page
        post, form, comment (dict): validated post and form data rendered to dictionary
    """
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # a comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # create a comment object without saving it to the database
        comment = form.save(commit=False)
        # assign the post to the comment
        comment.post = post
        # save the comment to the database
        comment.save()
    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )
