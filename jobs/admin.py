from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Job, Application, Resume, TrustedCompany

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
    list_display = ('title', 'employer', 'location', 'job_type', 'is_active', 'is_featured', 'created_at')
    list_filter = ('job_type', 'category', 'is_active', 'is_featured')
    search_fields = ('title', 'description', 'employer__username', 'employer__company_name')
    list_editable = ('is_featured', 'is_active')
    list_per_page = 20


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'job_seeker', 'status', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('job__title', 'job_seeker__username', 'job_seeker__email')
    readonly_fields = ('applied_at', 'updated_at')


class TrustedCompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'title', 'is_primary', 'uploaded_at')
    list_filter = ('is_primary', 'uploaded_at')
    search_fields = ('job_seeker__username', 'title')


# Register all models - ONLY ONCE each
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(TrustedCompany, TrustedCompanyAdmin)