from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.core.paginator import Paginator
from .models import CustomUser, Job, Application, Resume, TrustedCompany
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser, Job, Application, Resume, SavedJob


def home(request):
    featured_jobs = Job.objects.filter(is_active=True, is_featured=True)[:6]
    recent_jobs = Job.objects.filter(is_active=True).order_by('-created_at')[:3]
    trusted_companies = TrustedCompany.objects.filter(is_active=True)
    
    context = {
        'featured_jobs': featured_jobs,
        'recent_jobs': recent_jobs,
        'trusted_companies': trusted_companies,
    }
    return render(request, 'jobs/home.html', context)
def register(request):
    """User registration - handles multi-step form data with optional profile picture and resume"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        # Get basic user data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user_type = request.POST.get('user_type')
        phone_number = request.POST.get('phone_number', '')
        location = request.POST.get('location', '')
        bio = request.POST.get('bio', '')
        company_name = request.POST.get('company_name', '')
        
        # Validate passwords match
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'jobs/register.html')
        
        # Validate required fields
        if not all([first_name, last_name, email, username, password, user_type]):
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'jobs/register.html')
        
        # Check if user exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'jobs/register.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'jobs/register.html')
        
        # For employers, company name is required
        if user_type == 'employer' and not company_name:
            messages.error(request, 'Company name is required for employers.')
            return render(request, 'jobs/register.html')
        
        # Create user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            phone_number=phone_number,
            location=location,
            bio=bio,
        )
        
        # Set company name for employer
        if user_type == 'employer' and company_name:
            user.company_name = company_name
            user.save()
        
        # Handle profile picture upload
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']
            user.save()
        
        # Handle resume upload for job seekers
        if user_type == 'job_seeker' and request.FILES.get('resume'):
            Resume.objects.create(
                job_seeker=user,
                title=f"{first_name}'s Resume",
                resume_file=request.FILES['resume'],
                is_primary=True
            )
        
        # Log the user in
        login(request, user)
        messages.success(request, f'Welcome {first_name}! Your account has been created successfully.')
        
        # Redirect based on user type
        if user_type == 'employer':
            return redirect('post_job')
        else:
            return redirect('dashboard')
    
    return render(request, 'jobs/register.html')


def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            messages.success(request, f'Welcome back {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'jobs/login.html')


def logout_view(request):
    """User logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


@login_required
def dashboard(request):
    """User dashboard based on role"""
    if request.user.user_type == 'employer':
        jobs = Job.objects.filter(employer=request.user)
        applications = Application.objects.filter(job__in=jobs)
        context = {
            'jobs': jobs,
            'total_jobs': jobs.count(),
            'total_applications': applications.count(),
            'pending_applications': applications.filter(status='pending').count(),
            'recent_applications': applications[:5],
        }
        return render(request, 'jobs/dashboard.html', context)
    else:
        applications = Application.objects.filter(job_seeker=request.user)
        context = {
            'applications': applications,
            'total_applications': applications.count(),
        }
        return render(request, 'jobs/dashboard.html', context)


@login_required
def profile(request):
    """User profile page"""
    return render(request, 'jobs/profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        user.phone_number = request.POST.get('phone_number', '')
        user.location = request.POST.get('location', '')
        user.bio = request.POST.get('bio', '')
        
        if request.FILES.get('profile_picture'):
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    return render(request, 'jobs/edit_profile.html', {'user': request.user})


@login_required
def job_list(request):
    """List all active jobs with search and filters"""
    jobs = Job.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        jobs = jobs.filter(
            models.Q(title__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(location__icontains=search_query) |
            models.Q(employer__company_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'jobs': page_obj,
        'search_query': search_query,
    }
    return render(request, 'jobs/job_list.html', context)


@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    has_applied = False
    is_saved = False
    
    if request.user.is_authenticated:
        if request.user.user_type == 'job_seeker':
            has_applied = Application.objects.filter(job=job, job_seeker=request.user).exists()
            is_saved = SavedJob.objects.filter(job=job, user=request.user).exists()
    
    context = {
        'job': job,
        'has_applied': has_applied,
        'is_saved': is_saved,
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def post_job(request):
    """Post a new job (employers only)"""
    if request.user.user_type != 'employer':
        messages.error(request, 'Only employers can post jobs.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        location = request.POST.get('location')
        salary_min = request.POST.get('salary_min')
        salary_max = request.POST.get('salary_max')
        job_type = request.POST.get('job_type')
        category = request.POST.get('category')
        
        job = Job.objects.create(
            employer=request.user,
            title=title,
            description=description,
            requirements=requirements,
            location=location,
            salary_min=salary_min if salary_min else None,
            salary_max=salary_max if salary_max else None,
            job_type=job_type,
            category=category
        )
        messages.success(request, f'Job "{job.title}" posted successfully!')
        return redirect('my_jobs')
    
    return render(request, 'jobs/post_job.html')


@login_required
def my_jobs(request):
    """List jobs posted by employer"""
    if request.user.user_type != 'employer':
        return redirect('dashboard')
    
    jobs = Job.objects.filter(employer=request.user)
    return render(request, 'jobs/my_jobs.html', {'jobs': jobs})

@login_required
def apply_job(request, job_id):
    """Apply for a job with resume selection"""
    if request.user.user_type != 'job_seeker':
        messages.error(request, 'Only job seekers can apply for jobs.')
        return redirect('dashboard')
    
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    # Check  already applied
    if Application.objects.filter(job=job, job_seeker=request.user).exists():
        messages.error(request, 'You have already applied for this job.')
        return redirect('job_detail', job_id=job_id)
    
    # Get user xistin rsumes from the Resume model
    resumes = Resume.objects.filter(job_seeker=request.user)
    
    if request.method == 'POST':
        cover_letter = request.POST.get('cover_letter')
        resume_id = request.POST.get('resume_id')
        new_resume = request.FILES.get('resume')
        
        if resume_id:
            try:
                selected_resume = Resume.objects.get(id=resume_id, job_seeker=request.user)
                resume_file = selected_resume.resume_file
            except Resume.DoesNotExist:
                messages.error(request, 'Selected resume not found.')
                return render(request, 'jobs/apply_job.html', {
                    'job': job,
                    'resumes': resumes,
                    'has_resumes': resumes.exists()
                })
        elif new_resume:
            # Create a new resume from uploaded file
            new_resume_obj = Resume.objects.create(
                job_seeker=request.user,
                title=f"Resume for {job.title}",
                resume_file=new_resume,
                is_primary=False
            )
            resume_file = new_resume_obj.resume_file
        else:
            messages.error(request, 'Please select or upload a resume.')
            return render(request, 'jobs/apply_job.html', {
                'job': job,
                'resumes': resumes,
                'has_resumes': resumes.exists()
            })
        
        # Create the application
        application = Application.objects.create(
            job=job,
            job_seeker=request.user,
            cover_letter=cover_letter,
            resume=resume_file
        )
        
        messages.success(request, f'Successfully applied for {job.title}!')
        return redirect('my_applications')
    
    return render(request, 'jobs/apply_job.html', {
        'job': job,
        'resumes': resumes,
        'has_resumes': resumes.exists()
    })

@login_required
def my_applications(request):
    """List applications by job seeker"""
    if request.user.user_type != 'job_seeker':
        return redirect('dashboard')
    
    applications = Application.objects.filter(job_seeker=request.user)
    return render(request, 'jobs/my_applications.html', {'applications': applications})


@login_required
def view_applications(request, job_id):
    """View applications for a specific job (employers only)"""
    if request.user.user_type != 'employer':
        return redirect('dashboard')
    
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = Application.objects.filter(job=job)
    return render(request, 'jobs/applications_list.html', {'job': job, 'applications': applications})


@login_required
def update_application_status(request, application_id):
    """Update application status (employers only)"""
    if request.user.user_type != 'employer':
        return redirect('dashboard')
    
    application = get_object_or_404(Application, id=application_id, job__employer=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Application.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, f'Application status updated to {application.get_status_display()}')
    
    return redirect('view_applications', job_id=application.job.id)


@login_required
def manage_resumes(request):
    """Manage resumes for job seekers"""
    if request.user.user_type != 'job_seeker':
        messages.error(request, 'Only job seekers can manage resumes')
        return redirect('dashboard')
    
    resumes = Resume.objects.filter(job_seeker=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        resume_file = request.FILES.get('resume_file')
        is_primary = request.POST.get('is_primary') == 'on'
        
        if title and resume_file:
            if is_primary:
                Resume.objects.filter(job_seeker=request.user).update(is_primary=False)
            Resume.objects.create(
                job_seeker=request.user,
                title=title,
                resume_file=resume_file,
                is_primary=is_primary
            )
            messages.success(request, 'Resume uploaded successfully!')
        else:
            messages.error(request, 'Please provide title and file.')
        return redirect('manage_resumes')
    
    return render(request, 'jobs/manage_resumes.html', {'resumes': resumes})


@login_required
def delete_resume(request, resume_id):
    """Delete a resume"""
    resume = get_object_or_404(Resume, id=resume_id, job_seeker=request.user)
    resume.delete()
    messages.success(request, 'Resume deleted successfully!')
    return redirect('manage_resumes')


@login_required
def set_primary_resume(request, resume_id):
    """Set a resume as primary"""
    resume = get_object_or_404(Resume, id=resume_id, job_seeker=request.user)
    Resume.objects.filter(job_seeker=request.user).update(is_primary=False)
    resume.is_primary = True
    resume.save()
    messages.success(request, f'{resume.title} is now your primary resume')
    return redirect('manage_resumes')


# Static pages
def about(request):
    return render(request, 'jobs/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        messages.success(request, f'Thank you {name}! We\'ll get back to you soon.')
        return redirect('contact')
    return render(request, 'jobs/contact.html')


def pricing(request):
    return render(request, 'jobs/pricing.html')


def browse_candidates(request):
    return render(request, 'jobs/browse_candidates.html')


def career_advice(request):
    return render(request, 'jobs/career_advice.html')


def salary_guide(request):
    return render(request, 'jobs/salary_guide.html')


def interview_tips(request):
    return render(request, 'jobs/interview_tips.html')


def recruitment_solutions(request):
    return render(request, 'jobs/recruitment_solutions.html')


# ============ SAVE JOB FEATURE ============

@login_required
def save_job(request, job_id):
    """Save a job for later"""
    if request.user.user_type != 'job_seeker':
        messages.error(request, 'Only job seekers can save jobs.')
        return redirect('dashboard')
    
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    # Check if already saved
    saved, created = SavedJob.objects.get_or_create(user=request.user, job=job)
    
    if created:
        messages.success(request, f'"{job.title}" saved to your list!')
    else:
        saved.delete()
        messages.info(request, f'"{job.title}" removed from saved jobs.')
    
    return redirect('job_detail', job_id=job_id)


@login_required
def saved_jobs(request):
    """View all saved jobs"""
    if request.user.user_type != 'job_seeker':
        return redirect('dashboard')
    
    saved_jobs = SavedJob.objects.filter(user=request.user)
    return render(request, 'jobs/saved_jobs.html', {'saved_jobs': saved_jobs})


@login_required
def remove_saved_job(request, job_id):
    """Remove a saved job"""
    SavedJob.objects.filter(user=request.user, job_id=job_id).delete()
    messages.success(request, 'Job removed from saved list.')
    return redirect('saved_jobs')


# ============ EMAIL NOTIFICATIONS ============

def send_application_status_email(application, old_status, new_status):
    """Send email notification when application status changes"""
    try:
        subject = f'Application Status Update - {application.job.title}'
        message = f"""
        Hello {application.job_seeker.first_name or application.job_seeker.username},
        
        Your application for "{application.job.title}" at {application.job.employer.company_name} has been updated.
        
        Status changed from: {old_status}
        Status changed to: {new_status}
        
        Login to your JobBoard account to view more details.
        
        Best regards,
        JobBoard Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [application.job_seeker.email],
            fail_silently=True,
        )
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


@login_required
def update_application_status(request, application_id):
    """Update application status with email notification"""
    if request.user.user_type != 'employer':
        return redirect('dashboard')
    
    application = get_object_or_404(Application, id=application_id, job__employer=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        old_status = application.status
        
        if new_status in dict(Application.STATUS_CHOICES) and new_status != old_status:
            application.status = new_status
            application.save()
            
            # Send email notification
            send_application_status_email(application, old_status, new_status)
            
            messages.success(request, f'Application status updated to {application.get_status_display()}. Email notification sent to {application.job_seeker.email}.')
        else:
            messages.info(request, 'No changes made.')
    
    return redirect('view_applications', job_id=application.job.id)


# Add to your register view after creating user
def send_welcome_email(user):
    """Send welcome email to new user"""
    try:
        subject = f'Welcome to JobBoard, {user.first_name}!'
        message = f"""
        Hello {user.first_name or user.username},
        
        Welcome to JobBoard! We're excited to help you find your dream job.
        
        Here's what you can do:
        - Complete your profile
        - Upload your resume
        - Start applying for jobs
        - Track your applications
        
        Login here: http://127.0.0.1:8000/login/
        
        Best regards,
        JobBoard Team
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
        return True
    except Exception as e:
        print(f"Welcome email error: {e}")
        return False


from django.contrib.auth import get_user_model
from django.http import HttpResponse

def create_admin(request):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('Ade', 'adedirancfx@gmail.com', 'Adeseun')
        return HttpResponse("Superuser created! Username: Ade, Password: Adeseun")
    return HttpResponse("Superuser already exists!")