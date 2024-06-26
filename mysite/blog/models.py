from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    """PublishedManager adds both the default objects manager
    and the published custom manager to the Post model
    """

    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Post class defines database tables for posts of the blog application
class Post(models.Model):
    """Post class defines data related to blog posting in the blog application.

    Args:
        title (CharField): title of the blog post
        slug (SlugField): url-friendly truncated title of the blog post
        author (ForeignKey): references the default user model. deleting author deletes their posts
        body (TextField): main content of the blog post
        publish (DateTimeField): timestamp of when the blog post was published
        created (DateTimeField): timestamp of when the blog post was created
        updated (DateTimeField): timestamp of when the blog post was last modified

    Returns:
        CharField: returns the title of the blog post
    """

    class Status(models.TextChoices):
        """allows management of blog post status: DRAFT or PUBLISHED.
        Utilizes new options for declaring model field choices, updated in Django 5
        """

        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date="publish")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="blog_posts"
    )
    body = models.TextField()

    # records when the post was published
    publish = models.DateTimeField(default=timezone.now)

    # saves the date automatically when creating the post object
    created = models.DateTimeField(auto_now_add=True)

    # saves the date automatically, records when the post object was last updated
    updated = models.DateTimeField(auto_now=True)

    # defines draft or published status of post.
    # Utilizes new options for declaring model field choices, updated in Django 5
    status = models.CharField(
        max_length=2,
        # limits the choices to those in Status
        choices=Status,
        # sets the default status of the post as a DRAFT
        default=Status.DRAFT,
    )

    # for PublishedManager
    #   the default manager
    objects = models.Manager()
    #   custom manager
    published = PublishedManager()

    # for django-taggit TaggableManager
    tags = TaggableManager()

    class Meta:
        # sets default sort order reverse chronologically, newest posts first
        ordering = ["-publish"]
        # defines database index for the publish field
        # MySQL doesn't support index ordering, it would create a normal index
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    # dunderstring method returns the title of the post
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """get_absolute_url dynamically builds the url using the name defined in urlpatterns.
        It uses the year, month, day, and slug of the Post object as a positional argument.
        mysite/urls.py  defines blog namespace.
        blog/urls.py    defines post_detail url.

        Returns:
            string: url of blog post to retrieve
        """
        return reverse(
            "blog:post_detail",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )


class Comment(models.Model):
    """Comment stores user comments on posts.

    Args:
        post (ForeignKey): many-to-1 relationship - multiple comments for each post
        name (CharField): name of commentor can be up to 80 characters
        email (EmailField): email address of commentor
        body (TextField): main content of the comment
        created (DateTimeField): timestamp of when the comment was created
        updated (DateTimeField): timestamp of when the comment was last modified
        active (BooleanField): true by default, indicates visibility. False hides it.

    Returns:
        string: name of commentor and post commented on are returned
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()

    # saves the date automatically when creating the comment
    created = models.DateTimeField(auto_now_add=True)

    # saves the date automatically, records when the comment was last updated
    updated = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    class Meta:
        # sets default sort order chronologically, newest posts first
        ordering = ["created"]
        # defines database index for the created field
        indexes = [
            models.Index(fields=["created"]),
        ]

    def __str__(self):
        return f"Comment by {self.name} on {self.post}"
