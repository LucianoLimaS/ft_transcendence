from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Tournament, Participant
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Tournament, Participant
from django.core.exceptions import ObjectDoesNotExist

@login_required
def pong(request, game_id):
    if request.htmx:
        return render(request, 'pong.html', {'game_id': game_id})
    else:
        return render(request, 'pong.html', {'game_id': game_id})
    
def pongLocal(request):
    if request.htmx:
        return render(request, 'pong_local.html')
    else:
        return render(request, 'pong_local_full.html')
    
@login_required
def tournament_list(request):
    if request.method == 'POST':
        tournament_name = request.POST.get('tournament_name')
        tournament_size = int(request.POST.get('tournament_size'))
        if not tournament_name:
             tournament_name = "Tournament created by " + request.user.username
        tournament = Tournament.objects.create(name=tournament_name, created_by=request.user, size=tournament_size)
        return redirect('tournament_detail', tournament_id=tournament.id)
    
    tournaments = Tournament.objects.all()
    if request.htmx:
        return render(request, 'partials/tournament_list.html', {'tournaments': tournaments})
    return render(request, 'tournament_list.html', {'tournaments': tournaments})


@login_required
def tournament_detail(request, tournament_id):
    tournament = get_object_or_404(Tournament, id=tournament_id)
    user_is_participant = False
    try:
        participant = Participant.objects.get(tournament=tournament, user=request.user)
        user_is_participant = True
    except ObjectDoesNotExist:
        participant = None
    
    if request.method == 'POST':
        if not tournament.is_full:
            next_position = tournament.participants.count() + 1
            Participant.objects.create(tournament=tournament, user=request.user, position=next_position)
            
        return redirect('tournament_detail', tournament_id=tournament.id)

    matches = get_matches(tournament)
    if request.htmx:
        return render(request, 'partials/tournament_detail.html', {'tournament': tournament, 'user_is_participant':user_is_participant, 'matches':matches})
    
    return render(request, 'tournament_detail.html', {'tournament': tournament, 'user_is_participant':user_is_participant, 'matches':matches})
    
def get_matches(tournament):
    participants = list(tournament.participants.order_by('position'))
    num_participants = len(participants)
    matches = []
    
    if num_participants < 2:
      return matches
    
    if num_participants == 2:
      matches.append([[participants[0], participants[1]]])
      return matches

    round_participants = participants[:] # Copia a lista para nao modificar a original
    matches_per_round = num_participants // 2
    
    while len(round_participants) > 1:
      round_matches = []
      for i in range(matches_per_round):
        match = [round_participants[i], round_participants[len(round_participants) - 1 - i]]
        round_matches.append(match)
      matches.append(round_matches)
      round_participants = round_participants[:matches_per_round]  
      matches_per_round //= 2

    return matches