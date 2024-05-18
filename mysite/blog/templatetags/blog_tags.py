import markdown
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from ..models import Post

register = template.Library()


# this simple tag returns the number of posts published on the blog
@register.simple_tag
def total_posts():
    return Post.published.count()


# this inclusion tag displays the latest posts in the blog's sidebar
@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count=5):
    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


# this simple tag displays the posts with the most comments
@register.simple_tag
def get_most_commented_posts(count=5):
    return Post.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:count]


# this custom template filter supports Markdown syntax, converts it to HTML
# applies mark_safe function, use with caution to prevent security vulnerabilities
@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
