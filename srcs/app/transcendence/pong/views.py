from http.client import HTTPResponse
from urllib.parse import unquote
from django.http import JsonResponse
import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.views import View
from django.views.generic import DetailView, TemplateView

from .forms import PongRoomForm, TournamentForm
from .models import GameMode, Match, PongRoom, Tournament, TournamentParticipant
from django.contrib.auth.models import User

import asyncio
import websockets
import json

logger = logging.getLogger(__name__)

class PongSelectGameMode(LoginRequiredMixin, TemplateView):
    template_name = "pong/play.html"
    def get(self, request, *args, **kwargs):
        context = {"GameMode": GameMode.as_dict()}
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, "pong/play.html", context)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        game_mode = request.POST.get("game_mode")
        logger.info(f"Selected game_mode: {game_mode}")
        if game_mode == GameMode.LOCAL.value:
            room_name = f"Local-{get_random_string(8)}"
            room = PongRoom.objects.create(
                name=room_name, game_mode=GameMode.LOCAL.value
            )
            response = JsonResponse({
                "message": "Sala criada",
                "room_id": room.id,
            })
            return response
        else:
            logger.info(f"Redirecting to PongEnterView with game_mode: {game_mode}")
            return redirect("pong:pongenter", game_mode=game_mode)


class PongEnterView(LoginRequiredMixin, TemplateView):
    template_name = "pong/enter.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game_mode = kwargs.get("game_mode")

        logger.info(f"Pong enter view game_mode: {game_mode}")

        context["game_mode"] = game_mode
        context["GameMode"] = GameMode.as_dict()

        if game_mode == GameMode.TOURNAMENT.value:
            context["form"] = TournamentForm()
            context["tournaments"] = Tournament.objects.filter(is_active=True)
        else:
            context["form"] = PongRoomForm()
            context["rooms"] = PongRoom.objects.filter(
                game_mode=game_mode, is_active=True
            )
        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, "pong/enter.html", self.get_context_data(**kwargs))
        return self.render_to_response(self.get_context_data(**kwargs))

    async def send_websocket_message(self, message, request):

        '''Aqui deveria ser verificado se está em desenvolvimento ou produção para definir a uri,
        mas como estamos com pressa para entregar o projeto, vou deixar assim por enquanto,
        chama a primeira, se der erro chama a segunda.'''

        uri = f"ws://{request.get_host()}/ws/chatroom/public-chat?add_user=false"
        try:
            async with websockets.connect(uri) as websocket:
                await websocket.send(message)
                response = await websocket.recv()
                return response
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")
        
        uri = f"ws://daphne:8001/ws/chatroom/public-chat?add_user=false"
        try:
            async with websockets.connect(uri) as websocket:
                await websocket.send(message)
                response = await websocket.recv()
                return response
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")
        
        return None
        


    def post(self, request, *args, **kwargs):
        game_mode = kwargs.get("game_mode")

        # Prepare the message to send to the WebSocket
        name = request.POST.get("name")
        message = json.dumps({
            "csrfmiddlewaretoken": request.POST.get("csrfmiddlewaretoken"),
            "body": f"Foi criado a sala {name}, corre pra jogar!",
            "system_notification": True,  # Adiciona a chave system_notification
            "HEADERS": {
            "HX-Request": "true",
            "HX-Trigger": "chat_message_form",
            "HX-Trigger-Name": None,
            "HX-Target": "chat_message_form",
            "HX-Current-URL": "http://{request.get_host()}/",
            "X-CSRFToken": request.POST.get("csrfmiddlewaretoken")
            }
        })

                # Send the message to the WebSocket
        response = asyncio.run(self.send_websocket_message(message, request))
        logger.info(f"WebSocket response: {response}")

        logger.info(f"PongEnterView POST game_mode: {game_mode}")
        logger.info(f"PongEnterView POST data: {request.POST}")
        if game_mode == GameMode.TOURNAMENT.value:
            form = TournamentForm(request.POST)
            max_players = request.POST.get("max_players")
            if max_players in ["4", "8"] and form.is_valid():
                tournament = form.save(commit=False)
                tournament.max_players = int(max_players)
                tournament.save()
                return JsonResponse({"message":"sala criada"}, status=200)
            else:
                return JsonResponse({"message":"houve um erro na criacão da sala"}, status=400)
        else:
            form = PongRoomForm(request.POST)
            if form.is_valid():
                room = form.save(commit=False)
                room.game_mode = game_mode
                room.save()
                return JsonResponse({"message":"sala criada"}, status=200)
            else:
                return JsonResponse({"message":"houve um erro na criacão da sala"}, status=400)


class PongRoomView(LoginRequiredMixin, TemplateView):

    template_name = "pong/room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room_id = kwargs.get("room_id")
        try:
            room = PongRoom.objects.get(id=room_id)
            context["room"] = room
            context["game_mode"] = room.game_mode
        except PongRoom.DoesNotExist:
            context["room"] = None
            context["game_mode"] = None
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context["room"] is None:
            return redirect("pong:selectmode")
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, "pong/room.html", context)
        return self.render_to_response(context)


class PongTournamentView(LoginRequiredMixin, DetailView):
    model = Tournament
    template_name = "pong/tournament.html"
    context_object_name = "tournament"
    pk_url_kwarg = "tournament_id"

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        tournament = self.object
        participants = TournamentParticipant.objects.filter(tournament=tournament)
        context["user"] = self.request.user
        context["status"] = "active" if tournament.is_active else "finished"
        context["participants_slots"] = range(tournament.max_players)
        context["quarter_slots"] = (
            list(range(1, 5)) if tournament.max_players == 8 else []
        )
        context["semi_slots"] = list(range(1, 3))
        logger.info(
            f"Displaying tournament: {tournament.name} with {participants.count()}"
        )
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, "pong/tournament.html", context)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        tournament = self.get_object()
        return redirect("pong:pongtournament", tournament_id=tournament.id)

class PongEnterLocalTournamentView(LoginRequiredMixin, TemplateView):
    template_name = "pong/enterLocalTournament.html"

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, "pong/enterLocalTournament.html")
        return render(request, self.template_name)

class PongLocalTournamentView(LoginRequiredMixin, TemplateView):
    template_name = "pong/localTournament8p.html"

    def get(self, request, *args, **kwargs):
        template_path = "pong/localTournament8p.html"
        # else ADDERRORPAGE pagina de erro
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, template_path)
        return render(request, self.template_name)


def format_datetime(dt):
    """
    Formats a datetime object to a string in the format 'YYYY-MM-DD HH:MM'.
    """
    return timezone.localtime(dt).strftime("%Y-%m-%d %H:%M") if dt else None


class UserStatsView(LoginRequiredMixin, View):
    """
    Returns general user statistics in JSON format:
    - Last online time
    - Total matches played and won
    - Total tournaments played and won
    """

    def get(self, request):
        user = request.user
        last_online = format_datetime(user.last_login)
        total_matches = (
            Match.objects.filter(player1=user).count()
            + Match.objects.filter(player2=user).count()
        )
        total_wins = Match.objects.filter(winner=user).count()
        total_tournaments = TournamentParticipant.objects.filter(player=user).count()
        total_tournament_wins = TournamentParticipant.objects.filter(
            player=user, is_eliminated=False
        ).count()

        data = {
            "last_online": last_online,
            "total_matches": total_matches,
            "total_wins": total_wins,
            "total_tournaments": total_tournaments,
            "total_tournament_wins": total_tournament_wins,
        }
        return JsonResponse(data)


class UserHistoryView(LoginRequiredMixin, View):
    """
    Returns detailed user history in JSON format:
    - Match history with date, opponent, and result
    - Tournament history with date, tournament name, and result
    """

    def get(self, request):
        user = request.user

        # Match history
        matches = Match.objects.filter(player1=user) | Match.objects.filter(
            player2=user
        )
        match_history = [
            {
                "date": format_datetime(match.created_at),
                "opponent": (
                    match.player2.username
                    if match.player1 == user
                    else match.player1.username
                ),
                "result": "Won" if match.winner == user else "Lost",
            }
            for match in matches
        ]

        # Tournament history
        tournaments = TournamentParticipant.objects.filter(player=user)
        tournament_history = [
            {
                "date": format_datetime(tournament.tournament.created_at),
                "tournament": tournament.tournament.name,
                "result": "Won" if not tournament.is_eliminated else "Lost",
            }
            for tournament in tournaments
        ]

        data = {
            "matches": match_history,
            "tournaments": tournament_history,
        }
        return JsonResponse(data)


class UserMatchHistoryView(LoginRequiredMixin, TemplateView):
    template_name = "pong/match_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = kwargs.get("user_id")  # Fetch user_id from the route

        try:
            requested_user = User.objects.get(id=user_id)  # Retrieve the user by ID
        except User.DoesNotExist:
            context["error"] = f"User with ID {user_id} does not exist."
            context["match_history"] = []
            return context

        # Fetch match history for the specified user
        matches = Match.objects.filter(player1=requested_user) | Match.objects.filter(player2=requested_user)
        context["match_history"] = [
            {
                "date": format_datetime(match.created_at),
                "opponent": (
                    match.player2.username if match.player1 == requested_user else match.player1.username
                ),
                "result": "Won" if match.winner == requested_user else "Lost",
            }
            for match in matches
        ]
        context["requested_user"] = requested_user
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, "pong/match_history.html", context)
        return self.render_to_response(context)


class UserTournamentHistoryView(LoginRequiredMixin, TemplateView):
    template_name = "pong/tournament_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = kwargs.get("user_id")  # Fetch user_id from the route

        try:
            requested_user = User.objects.get(id=user_id)  # Retrieve the requested_user by ID
        except User.DoesNotExist:
            context["error"] = f"User with ID {user_id} does not exist."
            context["tournament_history"] = []
            return context

        # Fetch tournament history for the specified requested_user
        tournaments = TournamentParticipant.objects.filter(player=requested_user)
        context["tournament_history"] = [
            {
                "date": format_datetime(tournament.tournament.created_at),
                "tournament": tournament.tournament.name,
                "result": "Won" if not tournament.is_eliminated else "Lost",
            }
            for tournament in tournaments
        ]
        context["requested_user"] = requested_user
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, "pong/tournament_history.html", context)
        return self.render_to_response(context)
