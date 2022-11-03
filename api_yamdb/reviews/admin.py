from django.contrib import admin

from reviews.models import Review, Comment, Category, Genre, Title


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'text',
        'score',
        'pub_date',
    )
    search_fields = ('pub_date',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'author',
        'text',
        'pub_date',
    )
    search_fields = ('review',)
    list_filter = ('review',)
    empty_value_display = '-пусто-'
   

admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
