from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    
    # Job related
    path('jobs/', views.job_list, name='job_list'),
    path('job-detail/<int:job_id>/', views.job_detail, name='job_detail'),
    path('post-job/', views.post_job, name='post_job'),
    path('my-jobs/', views.my_jobs, name='my_jobs'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('applications/<int:job_id>/', views.view_applications, name='view_applications'),
    path('update-status/<int:application_id>/', views.update_application_status, name='update_application_status'),
    
    # Resume management
    path('manage-resumes/', views.manage_resumes, name='manage_resumes'),
    path('delete-resume/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('set-primary-resume/<int:resume_id>/', views.set_primary_resume, name='set_primary_resume'),
    
    # Static pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('browse-candidates/', views.browse_candidates, name='browse_candidates'),
    path('career-advice/', views.career_advice, name='career_advice'),
    # Add these to your urlpatterns
    path('save-job/<int:job_id>/', views.save_job, name='save_job'),
    path('saved-jobs/', views.saved_jobs, name='saved_jobs'),
    path('remove-saved-job/<int:job_id>/', views.remove_saved_job, name='remove_saved_job'),
    path('view-resume/<int:application_id>/', views.view_resume, name='view_resume'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)