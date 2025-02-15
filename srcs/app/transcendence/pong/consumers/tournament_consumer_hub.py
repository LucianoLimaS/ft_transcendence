import asyncio
import json
import logging
import random

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

# from django.contrib.auth import get_user_model
from pong.models import Match, PongRoom, Tournament, TournamentParticipant
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class TournamentConsumerHub(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tournament_lock = asyncio.Lock()

    async def connect(self):
        self.tournament_id = self.scope["url_route"]["kwargs"]["tournament_id"]
        self.tournament_group_name = f"tournament_{self.tournament_id}"
        self.user = self.scope["user"]

        if self.user.is_anonymous:
            await self.accept()
            await self.send(
                text_data=json.dumps(
                    {"type": "not_auth", "message": "User not authenticated"}
                )
            )
            logger.info("User not authenticated")
            await self.close()
        else:
            await self.channel_layer.group_add(
                self.tournament_group_name, self.channel_name
            )
            await self.accept()
            await self.update_and_send_state_to_group()
            logger.info(
                f"User {self.user.username} connected to tournament {self.tournament_id}: {self.tournament_group_name}"
            )

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.tournament_group_name, self.channel_name
        )
        logger.info(
            f"User {self.user.username} disconnected from tournament {self.tournament_id}: {self.tournament_group_name}"
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data["type"]

        if message_type == "join_tournament":
            async with self.tournament_lock:
                joined: bool = await self.handle_join_tournament()
                if joined:
                    await self.check_start_tournament()
                    await self.update_and_send_state_to_group()

    # Database methods
    @sync_to_async
    def get_tournament(self) -> Tournament:
        #preciso trazer junto o winner para pegar o username
         return Tournament.objects.select_related('winner').get(id=self.tournament_id)

    @sync_to_async
    def get_participants(self, tournament: Tournament) -> list:
        return list(tournament.participants.select_related("player").all())

    @sync_to_async
    def get_matches(self, tournament: Tournament) -> list:
        return list(
            Match.objects.filter(room__tournament=tournament)
            .select_related("player1", "player2", "winner", "room")
            .order_by("id")
        )

    @sync_to_async
    def tournament_participant_count(self, tournament: Tournament) -> int:
        return tournament.participants.count()

    @sync_to_async
    def create_participant(
        self, tournament: Tournament, user: User
    ) -> TournamentParticipant:
        return TournamentParticipant.objects.create(tournament=tournament, player=user)

    @sync_to_async
    def matches_exist_for_tournament(self, tournament: Tournament) -> bool:
        return Match.objects.filter(room__tournament=tournament).exists()

    @sync_to_async
    def save_match(self, match: Match) -> None:
        match.save()
    
    @sync_to_async
    def get_tournament_winner(self, tournament: Tournament) -> User:  
        return tournament.winner.username if tournament.winner else ""

    # handlers
    async def join_tournament_db(self) -> str:
        try:
            tournament = await self.get_tournament()
            if tournament:
                participants = await self.get_participants(tournament)
                already_joined = any(p.player == self.user for p in participants)
                if already_joined:
                    return "already_joined"
                count = await self.tournament_participant_count(tournament)
                if count < tournament.max_players:
                    await self.create_participant(tournament, self.user)
                    logger.info(
                        f"User {self.user.username} joined tournament {tournament.name}"
                    )
                    return "joined"
        except Exception as e:
            logger.exception(f"Error joining tournament {self.tournament_id}: {e}")
        return "error"

    async def handle_join_tournament(self) -> bool:
        joined = await self.join_tournament_db()
        if joined == "joined":
            message = f"{self.user.username} joined the tournament"
            await self.send_tournament_message_to_group(message)
            return True
        elif joined == "already_joined":
            await self.send_error("You already joined the tournament")
            return False
        else:
            await self.send_error(f"Error joining tournament {self.tournament_id}")
        return False

    # tounament logic
    async def check_start_tournament(self) -> None:
        tournament = await self.get_tournament()
        count = await self.tournament_participant_count(tournament)
        if count == tournament.max_players:
            await self.create_bracket_structure(tournament)
            # Reached the maximum number, now draw players in matches
            await self.assign_players_to_initial_matches(tournament)

            message = "Tournament will start soon!"
            await self.send_tournament_message_to_group(message)

    async def create_bracket_structure(self, tournament: Tournament):
        existing_matches = await self.matches_exist_for_tournament(tournament)
        if existing_matches:
            return

        max_players = tournament.max_players
        bracket_config = {
            4: [("Semi", 2), ("Final", 1)],
            8: [("Quarter", 4), ("Semi", 2), ("Final", 1)],
        }
        rounds = bracket_config.get(max_players, [])

        for round_name, match_count in rounds:
            for i in range(match_count):
                suffix = str(i + 1) if match_count > 1 else ""
                room_name = f"{tournament.name}-{round_name}{suffix}"

                room = await sync_to_async(PongRoom.objects.create)(
                    name=room_name,
                    game_mode="tournament",
                    tournament=tournament,
                )
                await sync_to_async(Match.objects.create)(
                    room=room, player1=None, player2=None
                )
                logger.info(f"Created match in round {round_name}: Room {room_name}")

    async def assign_players_to_initial_matches(self, tournament: Tournament):
        participants: list = await self.get_participants(tournament)
        random.shuffle(participants)

        matches = await self.get_matches(tournament)

        if tournament.max_players == 4:
            semi_matchs = matches[0:2]
            index = 0
            for match in semi_matchs:
                match.player1 = participants[index].player
                match.player2 = participants[index + 1].player
                await sync_to_async(match.save)()
                index += 2
                logger.info(f"Assigned players to match {match.id}")
                logger.info(f"Player1: {match.player1.username}")
                logger.info(f"Player2: {match.player2.username}")
        elif tournament.max_players == 8:
            quarter_matchs = matches[0:4]
            index = 0
            for match in quarter_matchs:
                match.player1 = participants[index].player
                match.player2 = participants[index + 1].player
                await sync_to_async(match.save)()
                index += 2
                logger.info(f"Assigned players to match {match.id}")
                logger.info(f"Player1: {match.player1.username}")
                logger.info(f"Player2: {match.player2.username}")

        await self.update_state_cache()

    # cache
    def state_cache_key(self):
        return f"tournament_{self.tournament_id}_state"

    async def update_state_cache(self):
        state = await self.get_current_state_data()
        cache.set(self.state_cache_key(), state)

    async def get_current_state_from_cache(self):
        state = cache.get(self.state_cache_key())
        if state:
            return state
        else:
            await self.update_state_cache()
            return cache.get(self.state_cache_key())

    async def update_and_send_state_to_group(self):
        await self.update_state_cache()
        await self.send_current_state_to_group()

    async def get_current_state_data(self):
        tournament = await self.get_tournament()
        participants = await self.get_participants(tournament)
        participant_list = [p.player.username for p in participants]
        matches = await self.get_matches(tournament)
        status = "active" if tournament.is_active else "finished"

        matches_info = []
        for match in matches:
            p1 = match.player1.username if match.player1 else "TBD"
            p2 = match.player2.username if match.player2 else "TBD"
            winner = match.winner.username if match.winner else None
            round_name = match.room.name.split("-")[
                -1
            ]  # Extrai o round do nome da sala

            matches_info.append(
                {
                    "id": match.id,
                    "player1": p1,
                    "player2": p2,
                    "room_id": match.room.id,
                    "finished": match.finished,
                    "winner": winner,
                    "round": round_name,
                }
            )
        
        # Determine the winner of the tournament
        tournament_winner = await self.get_tournament_winner(tournament)   

        return {
            "type": "current_state",
            "tournament_id": tournament.id,
            "tournament_name": tournament.name,
            "participants": participant_list,
            "max_players": tournament.max_players,
            "status": status,
            "matches": matches_info,
            "winner": tournament_winner,
        }

    # Methods to send messages to the group
    async def send_tournament_message_to_group(self, message: str):
        await self.channel_layer.group_send(
            self.tournament_group_name,
            {
                "type": "send_tournament_message",
                "message": message,
            },
        )
        logger.info(
            f"User {self.user.username} sent tournament message to group: {message}"
        )

    async def send_current_state_to_group(self):
        state = await self.get_current_state_from_cache()
        await self.channel_layer.group_send(
            self.tournament_group_name,
            {
                "type": "send_tournament_current_state",
                "state": state,
            },
        )
        logger.info(f"User {self.user.username} sent current state to group: {state}")

    # Methods to send messages to the client
    async def send_tournament_message(self, event):
        message = event["message"]
        await self.send(
            text_data=json.dumps({"type": "tournament_message", "message": message})
        )

    async def send_current_state_to_self(self):
        state = await self.get_current_state_from_cache()
        if self.user.username in state["participants"]:
            await self.send(text_data=json.dumps({"type": "joined"}))
        await self.send(text_data=json.dumps({"type": "current_state", "state": state}))
        logger.info(f"{self.user.username} sent_current_state_to_self: {state}")

    async def send_tournament_current_state(self, event):
        state = event["state"]
        await self.send(text_data=json.dumps({"type": "current_state", "state": state}))

    async def send_error(self, message: str) -> None:
        """
        Sends an error message to the client.

        Args:
            message (str): The error message to send.
        """
        await self.send(text_data=json.dumps({"type": "error", "message": message}))
