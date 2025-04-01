from django.contrib import admin
from .models import Stock, WhatsAppLead
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    # Enable filtering/searching by username in the admin panel
    search_fields = ('username',)

admin.site.register(Stock)
admin.site.register(WhatsAppLead)

# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

