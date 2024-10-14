from django.contrib import admin
from .models.user import Member 
# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'last_login', 'deadline_from', 'deadline_to')  # Fields to display in the list view
    list_filter = ('is_active', 'deadline_from', 'deadline_to')  # Fields to filter by
    search_fields = ('email', 'name')

admin.site.register(Member, MemberAdmin)