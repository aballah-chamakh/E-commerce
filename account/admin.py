from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import User,Profile,CustomerProfile,ParaProfile

profiles_models = [Profile,CustomerProfile,ParaProfile]

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'username','admin','selling_point')
    list_filter = ('admin','selling_point')
    fieldsets = (
        (None, {'fields': ('email','username', 'password')}),
        ('Personal info', {'fields': ('selling_point',)}),
        ('Permissions', {'fields': ('active','staff','admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username','password1', 'password2','selling_point')}
        ),
    )
    search_fields = ('email',)
    ordering = ('admin',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
for model in profiles_models :
    admin.site.register(model)
