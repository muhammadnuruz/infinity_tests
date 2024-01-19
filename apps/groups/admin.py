# from django.contrib import admin
# from django.contrib.auth.models import Group as _
# from apps.groups.models import Groups
# from apps.users.models import User
#
#
# class AnswersInline(admin.StackedInline):
#     model = User
#
#
# class GroupsAdmin(admin.ModelAdmin):
#     list_display = ('name', 'created_at')
#     inlines = [AnswersInline]
#
#
# admin.site.unregister(_)
# admin.site.register(Groups, GroupsAdmin)
