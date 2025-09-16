from django.contrib import admin
from .models import Movie, Review


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name', 'description']
    list_display = ('id', 'name', 'price')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'user', 'short_comment', 'date', 'is_flagged')
    list_filter = ('is_flagged', 'date', 'movie')
    search_fields = ('movie__name', 'user__username', 'comment')
    date_hierarchy = 'date'
    ordering = ['-date']
    actions = ['unflag_reviews', 'flag_reviews']

    def short_comment(self, obj):
        return (obj.comment[:60] + '…') if len(obj.comment) > 60 else obj.comment
    short_comment.short_description = 'Comment'

    def unflag_reviews(self, request, queryset):
        updated = queryset.update(is_flagged=False)
        self.message_user(request, f"Unflagged {updated} review(s).")
    unflag_reviews.short_description = "Unflag selected reviews"

    def flag_reviews(self, request, queryset):
        updated = queryset.update(is_flagged=True)
        self.message_user(request, f"Flagged {updated} review(s).")
    flag_reviews.short_description = "Flag selected reviews"