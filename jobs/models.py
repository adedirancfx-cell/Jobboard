from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='job_seeker')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username


class Job(models.Model):
    JOB_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('remote', 'Remote'),
        ('internship', 'Internship'),
    )
    
    CATEGORY_CHOICES = (
        ('tech', 'Technology'),
        ('finance', 'Finance'),
        ('healthcare', 'Healthcare'),
        ('education', 'Education'),
        ('marketing', 'Marketing'),
        ('design', 'Design'),
        ('sales', 'Sales'),
        ('other', 'Other'),
    )
    
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=200)
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Amount in Nigerian Naira (₦)")
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Amount in Nigerian Naira (₦)")
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False, help_text="Show this job on homepage featured section")
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']


class Application(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('interview', 'Interview Scheduled'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    job_seeker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    notification_sent = models.BooleanField(default=False)
    last_status_update = models.DateTimeField(auto_now=True)

    
    class Meta:
        unique_together = ['job', 'job_seeker']
        ordering = ['-applied_at']
    
    def __str__(self):
        return f"{self.job_seeker.username} - {self.job.title}"
    
class TrustedCompany(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company_logos/')
    website_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = "Trusted Companies"
    
    def __str__(self):
        return self.name    
    


class Resume(models.Model):
    """Job seeker's resume/CV model"""
    job_seeker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200, help_text="e.g., 'Frontend Developer Resume', 'CV - 2024'")
    resume_file = models.FileField(upload_to='resumes/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_primary', '-uploaded_at']
    
    def __str__(self):
        return f"{self.job_seeker.username} - {self.title}"
    
    def save(self, *args, **kwargs):
        # If this resume is set as primary, remove primary flag from other resumes
        if self.is_primary:
            Resume.objects.filter(job_seeker=self.job_seeker, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)    


# Add to models.py

class Resume(models.Model):
    """Job seeker's resume/CV model"""
    job_seeker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='resumes')
    title = models.CharField(max_length=200, help_text="e.g., 'Frontend Developer Resume'")
    resume_file = models.FileField(upload_to='resumes/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', '-uploaded_at']
    
    def __str__(self):
        return f"{self.job_seeker.username} - {self.title}"     

class SavedJob(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'job']
        ordering = ['-saved_at']
    
    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"       