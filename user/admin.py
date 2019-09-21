from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import User

class MyUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'firm')
    list_filter = ('is_superuser',)
    list_display_links = ('first_name', 'last_name','email')
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personel Info', {'fields': ('email','first_name','last_name','phone','address','image','firm')}),
        ('Permissions', {'fields': ('user_permissions',)}),
        ('Authority', {'fields': ('is_active','is_staff','is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ('user_permissions',)



admin.site.site_header = "MstGnz"
admin.site.register(User, MyUserAdmin)
admin.site.unregister(Group)
