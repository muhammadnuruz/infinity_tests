from django.contrib import admin

from apps.topics.models import Topics


class TopicsAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name',)
    ordering = ('name',)


admin.site.register(Topics, TopicsAdmin)
