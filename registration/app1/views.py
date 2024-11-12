from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app1.models import Record
from .forms import CustomUserCreationForm, CustomAuthenticationForm, DashboardDataForm, RecordForm
from django.contrib.auth.models import User  # Ensure to import User model

def register_view(request):
    """Handles user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
        else:
            # Show validation errors
            messages.error(request, 'There was an error with your registration. Please correct the issues below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'app1/register.html', {'form': form})

def login_view(request):
    """Handles user login."""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()

    return render(request, 'app1/login.html', {'form': form})

@login_required
def home_view(request):
    """Renders the home page with dashboard content and allows updates for authenticated users."""
    if request.method == 'POST':
        form = DashboardDataForm(request.POST)
        if 'save' in request.POST and form.is_valid():
            # Save form data to session
            request.session['recent_activity'] = form.cleaned_data['recent_activity']
            request.session['status_info'] = form.cleaned_data['status_info']
            request.session['tasks_info'] = form.cleaned_data['tasks_info']
            messages.success(request, 'Dashboard data saved successfully!')
            return redirect('home')
        elif 'cancel' in request.POST:
            messages.info(request, 'Changes canceled.')
            return redirect('home')
    else:
        # Load form with current session data
        form = DashboardDataForm(initial={
            'recent_activity': request.session.get('recent_activity', 'No recent activity yet.'),
            'status_info': request.session.get('status_info', 'All systems are operational.'),
            'tasks_info': request.session.get('tasks_info', 'You have 3 pending tasks.')
        })

    # Retrieve records for the currently logged-in user only
    records = Record.objects.filter(user=request.user)

    context = {
        'form': form,
        'records': records,
    }

    return render(request, 'app1/home.html', context)

def logout_view(request):
    """Logs out the user and redirects to the login page."""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

def dashboard(request):
    """Additional dashboard view if needed."""
    return render(request, 'app1/dashboard.html')

@login_required
def upload_record(request):
    """Handles the upload of records with images."""
    if request.method == 'POST' and request.FILES.get('image'):
        form = RecordForm(request.POST, request.FILES)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user  # Associate the record with the current user
            record.save()
            messages.success(request, 'Record uploaded successfully!')
            return redirect('home')
        else:
            messages.error(request, 'There was an issue with the file upload. Please check your data and try again.')
    else:
        form = RecordForm()

    return render(request, 'app1/upload_record.html', {'form': form})
