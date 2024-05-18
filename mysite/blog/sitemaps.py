from django.contrib.sitemaps import Sitemap

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
