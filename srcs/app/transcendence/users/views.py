from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
#from allauth.account.utils import send_email_confirmation
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from .forms import *
from django.http import JsonResponse, HttpResponse

def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile
    else:
        try:
            profile = request.user.profile
        except:
            return redirect_to_login(request.get_full_path())
    return render(request, 'users/profile.html', {'profile':profile})

def public_profile_view(request, userId=None):
    try:
        #profile = request.user.profile
        data = {
        "profileImageSrc": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSZmIuaRfZgN-nCpwp6rmPmhYrpz9ajvUN-w&s",
        "username": "Gamer123",
        "userId": userId,
        "numberOfFriends": 42,
        "statusFriend": "pendente",
        "matchStatistic": {
            "totalGamesPlayed": 150,
            "totalWins": 90,
            "totalLosses": 60,
            "winRatePercentage": 60
        },
        "tournamentStatistic": {
            "totalTournamentParticipations": 20,
            "totalTournamentWins": 5,
            "totalTop3Finishes": 10
        },
        "badges": [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSZmIuaRfZgN-nCpwp6rmPmhYrpz9ajvUN-w&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSZmIuaRfZgN-nCpwp6rmPmhYrpz9ajvUN-w&s",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSZmIuaRfZgN-nCpwp6rmPmhYrpz9ajvUN-w&s"
        ],
        "matchHistory": [
            {"opponentName": "Player1", "status": "victory", "score": "3-1"},
            {"opponentName": "Player2", "status": "Defeat", "score": "2-3"},
            {"opponentName": "Player3", "status": "victory", "score": "3-0"},
            {"opponentName": "Player4", "status": "victory", "score": "3-2"},
            {"opponentName": "Player5", "status": "Defeat", "score": "1-3"}
        ]
    }

        return JsonResponse(data, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)  
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
        
    if request.path == reverse('profile-onboarding'):
        onboarding = True
    else:
        onboarding = False
      
    return render(request, 'users/profile_edit.html', { 'form':form, 'onboarding':onboarding })


@login_required
def profile_settings_view(request):
    return render(request, 'users/profile_settings.html')


@login_required
def profile_emailchange(request):
    
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partials/email_form.html', {'form':form})
    
    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)

        if form.is_valid():
            
            # Check if the email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} is already in use.')
                return redirect('profile-settings')
            
            form.save() 
            
            # Then Signal updates emailaddress and set verified to False
            
            # Then send confirmation email 
            #send_email_confirmation(request, request.user)
            
            return redirect('profile-settings')
        else:
            messages.warning(request, 'Form not valid')
            return redirect('profile-settings')
        
    return redirect('home')


@login_required
def profile_emailverify(request):
    #send_email_confirmation(request, request.user)
    return redirect('profile-settings')


@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == "POST":
        logout(request)
        user.delete()
        messages.success(request, 'Account deleted, what a pity')
        return redirect('home')
    
    return render(request, 'users/profile_delete.html')