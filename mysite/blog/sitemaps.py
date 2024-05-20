from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from taggit.models import Tag

from .models import Post


class PostSitemap(Sitemap):
    """PostSitemap defines a custom sitemap, inheriting the Sitemap class of the
    sitemaps module. The attributes changefreq and priority indicate the change
    frequency of post pages and their relevance in the site (max value is 1).
    """

    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated


class TagSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.7

    def items(self):
        return Tag.objects.all()

    def location(self, obj):
        return reverse("blog:post_list_by_tag", args=[obj.slug])
