from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Job, Application

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'company_name', 'location', 'is_active')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'company_name')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('user_type', 'phone_number', 'company_name', 'profile_picture', 'bio', 'location')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile Information', {
            'fields': ('user_type', 'phone_number', 'company_name', 'location')
        }),
    )

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'location', 'job_type', 'category', 'is_active', 'created_at')
    list_filter = ('job_type', 'category', 'is_active', 'location')
    search_fields = ('title', 'description', 'employer__username', 'employer__company_name')
    readonly_fields = ('created_at', 'updated_at')

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'job_seeker', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('job__title', 'job_seeker__username', 'job_seeker__email')
    readonly_fields = ('applied_at', 'updated_at')

from .models import CustomUser, Job, Application, TrustedCompany

# Add this class before admin.site.register
class TrustedCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

# Register
admin.site.register(TrustedCompany, TrustedCompanyAdmin)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)