from django.contrib import admin
from apps.tests.models import Tests, Answers


class AnswersInline(admin.StackedInline):
    model = Answers
    extra = 0


class TestsAdmin(admin.ModelAdmin):
    list_display = ('question', 'topic', 'created_at', 'updated_at')
    list_filter = ('topic', 'created_at')
    inlines = [AnswersInline]


class AnswersAdmin(admin.ModelAdmin):
    list_display = ('answer', 'is_correct', 'test', 'created_at', 'updated_at')
    list_filter = ('test', 'is_correct', 'created_at')


admin.site.register(Tests, TestsAdmin)
admin.site.register(Answers, AnswersAdmin)
