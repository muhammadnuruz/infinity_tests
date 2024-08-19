from django.contrib import admin

from apps.words.models import Words


class WordsAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)


admin.site.register(Words, WordsAdmin)
