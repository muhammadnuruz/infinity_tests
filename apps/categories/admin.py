from django.contrib import admin

from apps.words.models import Words
from apps.categories.models import Categories


class WordsInline(admin.StackedInline):
    model = Words
    extra = 1


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    ordering = ('name', 'created_at')
    inlines = [WordsInline]


admin.site.register(Categories, CategoriesAdmin)
