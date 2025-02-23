from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib.auth.views import redirect_to_login
from django.contrib import messages
from .forms import *
from django.http import JsonResponse, HttpResponse
from .models import Profile, Friendship, Block
from pong.models import Match, TournamentParticipant, Tournament  # Adicione a importação do modelo Tournament
from django.db import models

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
        user = get_object_or_404(User, id=userId)
        profile = get_object_or_404(Profile, user=user)

        # Número de amigos
        number_of_friends = Friendship.objects.filter(from_user=user, accepted=True).count()

        # Status de amizade
        friendship = Friendship.objects.filter(from_user=request.user, to_user=user).first()
        if friendship:
            status_friend = "accepted" if friendship.accepted else "pending"
        else:
            status_friend = "no_friendship"

        # Verificar se o usuário está bloqueado
        is_blocked = Block.objects.filter(blocker=request.user, blocked=user).exists()

        # Estatísticas de partidas
        total_games_played = Match.objects.filter(models.Q(player1=user) | models.Q(player2=user)).count()
        total_wins = Match.objects.filter(winner=user).count()
        total_losses = total_games_played - total_wins
        win_rate_percentage = (total_wins / total_games_played) * 100 if total_games_played > 0 else 0

        # Estatísticas de torneios
        total_tournament_participations = TournamentParticipant.objects.filter(player=user).count()
        total_tournament_wins = Tournament.objects.filter(winner=user).count()
        total_top3_finishes = TournamentParticipant.objects.filter(player=user, is_eliminated=False).count()

        # Insígnias (badges) - Exemplo estático, ajuste conforme necessário
        badges = [
            "/static/assets/cow_savior_icon.png",
            "/static/assets/towel_icon.png",
        ]

        # Histórico de partidas
        matches = Match.objects.filter(models.Q(player1=user) | models.Q(player2=user))
        match_history = []
        for match in matches:
            opponent = match.player2 if match.player1 == user else match.player1
            status = "victory" if match.winner == user else "Defeat"
            score = "N/A"  # Ajuste conforme necessário
            match_history.append({
                "opponentName": opponent.username if opponent else "N/A",
                "status": status,
                "score": score
            })

        data = {
            "profileImageSrc": profile.avatar,
            "username": user.username,
            "displayname": profile.displayname,
            "userId": userId,
            "numberOfFriends": number_of_friends,
            "statusFriend": status_friend,
            "isBlocked": is_blocked,
            "matchStatistic": {
                "totalGamesPlayed": total_games_played,
                "totalWins": total_wins,
                "totalLosses": total_losses,
                "winRatePercentage": win_rate_percentage
            },
            "tournamentStatistic": {
                "totalTournamentParticipations": total_tournament_participations,
                "totalTournamentWins": total_tournament_wins,
                "totalTop3Finishes": total_top3_finishes
            },
            "badges": badges,
            "matchHistory": match_history
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