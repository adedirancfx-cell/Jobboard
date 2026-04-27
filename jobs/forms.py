from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Job, Application, Resume

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}))
    
    # Optional fields
    phone_number = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}))
    location = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}), required=False)
    company_name = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}))
    
    # Profile picture - OPTIONAL
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white file:bg-purple-600 file:text-white file:px-4 file:py-2 file:rounded file:border-0'}))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 
                  'user_type', 'phone_number', 'company_name', 'location', 'bio', 'profile_picture']
    
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        company_name = cleaned_data.get('company_name')
        
        if user_type == 'employer' and not company_name:
            self.add_error('company_name', 'Company name is required for employers')
        return cleaned_data


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'location', 
                  'salary_min', 'salary_max', 'job_type', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}),
            'requirements': forms.Textarea(attrs={'rows': 5, 'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}),
            'salary_min': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white', 'placeholder': '$50,000'}),
            'salary_max': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white', 'placeholder': '$80,000'}),
            'job_type': forms.Select(attrs={'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}),
        }


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'resume_file', 'is_primary']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white', 'placeholder': 'e.g., My Resume - 2024'}),
            'resume_file': forms.FileInput(attrs={'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white', 'accept': '.pdf,.doc,.docx'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-purple-600 rounded focus:ring-purple-500'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 6, 'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white', 'placeholder': 'Why are you a good fit for this role?'}),
            'resume': forms.FileInput(attrs={'class': 'w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white', 'accept': '.pdf,.doc,.docx'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'location', 'bio', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}),
            'phone_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}),
            'location': forms.TextInput(attrs={'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}),
            'profile_picture': forms.FileInput(attrs={'class': 'w-full px-4 py-2 bg-white/10 border border-white/20 rounded-lg focus:border-purple-500 focus:outline-none text-white'}),
        }