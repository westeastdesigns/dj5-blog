from django.contrib import admin

from .models import Post


# Registers models for the blog application
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    # Show Facets is a new feature introduced in Django 5, shows count in filter
    show_facets = admin.ShowFacets.ALWAYS
    