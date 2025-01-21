import json
import logging

from asgiref.sync import sync_to_async
from django.core.cache import cache
from pong.models import Match, PongRoom, Tournament, TournamentParticipant
from django.contrib.auth.models import User

from .online_consumer import OnlinePongConsumer
from .base_consumer import (
    Paddle,
    GameStateEvent,
)

logger = logging.getLogger(__name__)


class TournamentPongConsumer(OnlinePongConsumer):
    # Methods to interact with the database
    @sync_to_async
    def get_first_match_by_room(self, room):
        return Match.objects.filter(room=room).first()

    @sync_to_async
    def get_tournament_by_id(self, tournament_id):
        return TournamentParticipant.objects.get(id=tournament_id)

    @sync_to_async
    def get_match_with_related(self, match_id: int) -> Match:
        return Match.objects.select_related(
            "room__tournament", "player1", "player2"
        ).get(id=match_id)

    @sync_to_async
    def eliminate_player(self, tournament: Tournament, user: User) -> None:
        return tournament.participants.filter(player=user).update(is_eliminated=True)

    @sync_to_async
    def get_alive_count(self, tournament: Tournament) -> int:
        return tournament.participants.filter(is_eliminated=False).count()

    @sync_to_async
    def finalize_tournament(self, tournament: Tournament) -> None:
        tournament.is_active = False
        tournament.save()

    @sync_to_async
    def get_winner(self, match):
        """
        Retrieves the winner of the match.
        """
        return match.winner

    async def start_game(self) -> bool:
        """
        Starts the game when both players are ready.
        In tournament mode, the game only starts when both players are ready, and the match ID is fetched from the database.
        """
        try:
            if not self.is_ready:
                async with self.ready_lock:
                    self.ready_players = cache.get(
                        f"{self.room_group_name}_ready_players", 0
                    )
                    self.ready_players += 1
                    self.is_ready = True
                    cache.set(
                        f"{self.room_group_name}_ready_players", self.ready_players
                    )
                    logger.info(
                        f"Player {self.scope['user'].id} is ready. Total ready players: {self.ready_players}"
                    )

                    if self.ready_players == 2:
                        room = await self.get_room_by_id(self.room_id)
                        self.match_id = cache.get(
                            f"{self.room_group_name}_match_id", None
                        )
                        match = await self.get_first_match_by_room(room)

                        self.had_a_match = cache.get(
                            f"{self.room_group_name}_had_a_match", False
                        )
                        self.had_a_match = True
                        self.had_a_match = cache.set(
                            f"{self.room_group_name}_had_a_match", self.had_a_match
                        )

                        if not match:
                            raise Exception("No match found for the given room.")

                        self.match_id = match.id
                        cache.set(f"{self.room_group_name}_match_id", self.match_id)
                        logger.info(f"Match ID set to {self.match_id}")
                        await self.worker_start_game()
                        return True
        except Exception as e:
            await self.send_error("Failed to start game.")
            logger.exception(f"Failed to start game: {e}")
        return False

    async def define_winner(self, event) -> None:
        """
        Defines the winner of the tournament match and redirects the player to the tournament hub.
        """
        try:
            await super().define_winner(event)
            room = await self.get_room_by_id(self.room_id)
            match = await self.get_first_match_by_room(room)
            await self.advance_tournament(match.id)
            await self.redirect_to_hub()
        except Exception as e:
            await self.send_error("Failed to define winner in tournament.")
            logger.exception(f"Failed to define winner in tournament: {e}")

    async def redirect_to_hub(self) -> None:
        """
        Redirects the player back to the tournament hub after the match concludes.
        """
        try:
            room = await self.get_room_by_id(self.room_id)
            tournament_id = room.tournament.id
            if tournament_id:
                tournament_url = f"/tournament/{tournament_id}/"
                await self.send_redirect(tournament_url)
            logger.info(f"Redirecting player to tournament hub at {tournament_url}")
        except PongRoom.DoesNotExist:
            await self.send_error("Room not found for redirection.")
            logger.error("Room not found when attempting to redirect to hub.")
        except AttributeError:
            await self.send_error("Tournament ID not found for redirection.")
            logger.error(
                "Tournament ID not found in room when attempting to redirect to hub."
            )

    async def finish_game(self) -> None:
        """
        Performs any necessary cleanup when the game ends.
        """
        try:
            self.had_a_match = cache.get(
                f"{self.room_group_name}_had_a_match", False
            )
            self.connected_players = cache.get(
                f"{self.room_group_name}_connected_players", {}
            )
            # printar todas as variaveis de cache

            if self.scope["user"].id in self.connected_players:
                if self.had_a_match:
                    # defines the other player as the winner
                    other_player = Paddle.RIGHT if self.player_paddle == Paddle.LEFT else Paddle.LEFT
                    # Send the winner message to the group
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "send_winner",
                            "game_state": {"winner": other_player},
                        },
                    )

                    #notify the other player that he won
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "send_alert_message",
                            "message": "The other player disconnected!",
                        },
                    )

                    # Send a message to the worker to finish the game
                    await self.channel_layer.send(
                        "pong_update_channel",
                        {
                            "type": "finish_game",
                            "room_id": str(self.room_id),
                        },
                    )

                    # Set the room as inactive 
                    await self.set_room_inactive()
                
                self.connected_players[self.scope["user"].id] = False
                cache.set(
                    f"{self.room_group_name}_connected_players", self.connected_players
                )
                
            #check if all players are disconnected
            all_disconnected = all(not connected for connected in self.connected_players.values())

            if all_disconnected:
                # Clear the cache of game-related variables
                cache.delete(f"{self.room_group_name}_players")
                cache.delete(f"{self.room_group_name}_game_data")
                cache.delete(f"{self.room_group_name}_ready_players")
                cache.delete(f"{self.room_group_name}_match_id")
                cache.delete(f"{self.room_group_name}_connected_players")
                cache.delete(f"{self.room_group_name}_had_a_match")
                logger.info(
                    f"Game finished and cleaned up for room {self.room_group_name}"
                )

            if self.room_group_name:
                # Remove the user from the group
                await self.channel_layer.group_discard(
                    self.room_group_name, self.channel_name
                )
                logger.info(f"User {self.scope['user']} disconnected from room {self.room_group_name}")
        except Exception as e:
            await self.send_error("Failed to finish game.")
            logger.exception(f"Failed to finish game: {e}")

    async def get_bracket_mapping(self, tournament: Tournament):

        # Retorna um dicionário indicando para onde vai o vencedor de cada partida.
        # Formato: {match_id: (next_match_id, player_slot)}
        # player_slot = 1 ou 2, indicando se o vencedor vai em player1 ou player2 da próxima match.

        matches = await sync_to_async(list)(
            Match.objects.filter(room__tournament=tournament).order_by("id")
        )

        if tournament.max_players == 4:
            # Supondo que as partidas são criadas na ordem: Semi1, Semi2, Final
            # Recupera os IDs após criação do bracket
            semi1, semi2, final = matches[:3]
            return {
                semi1.id: (final.id, 1),  # Vencedor Semi1 -> Final.player1
                semi2.id: (final.id, 2),  # Vencedor Semi2 -> Final.player2
            }
        elif tournament.max_players == 8:
            # Supondo que as partidas são criadas na ordem: QF1-4, Semi1-2, Final
            quarter_finals = matches[:4]
            semi_finals = matches("id")[4:6]
            final = matches("id")[6]
            return {
                quarter_finals[0].id: (
                    semi_finals[0].id,
                    1,
                ),  # Vencedor QF1 -> Semi1.player1
                quarter_finals[1].id: (
                    semi_finals[0].id,
                    2,
                ),  # Vencedor QF2 -> Semi1.player2
                quarter_finals[2].id: (
                    semi_finals[1].id,
                    1,
                ),  # Vencedor QF3 -> Semi2.player1
                quarter_finals[3].id: (
                    semi_finals[1].id,
                    2,
                ),  # Vencedor QF4 -> Semi2.player2
                semi_finals[0].id: (final.id, 1),  # Vencedor Semi1 -> Final.player1
                semi_finals[1].id: (final.id, 2),  # Vencedor Semi2 -> Final.player2
            }

    async def advance_tournament(self, match_id: int):
        match = await self.get_match_with_related(match_id)
        tournament = match.room.tournament

        winner = await self.get_winner(match)

        loser = match.player1 if match.player1 != winner else match.player2
        await self.eliminate_player(tournament, loser)

        alive_count = await self.get_alive_count(tournament)
        if alive_count == 1:
            tournament.winner = winner
            await self.finalize_tournament(tournament)
        else:
            bracket_mapping = await self.get_bracket_mapping(tournament)

            if match.id in bracket_mapping:
                next_match_index, player_slot = bracket_mapping[match.id]
                next_match = await self.get_match_with_related(next_match_index)
                if player_slot == 1:
                    next_match.player1 = winner
                else:
                    next_match.player2 = winner

                await sync_to_async(next_match.save)()
                logger.info(
                    f"Assigned winner {match.winner.username} to match {next_match.id} as player {player_slot}"
                )

    # Methods to send messages to the client
    async def send_redirect(self, url: str) -> None:
        """
        Sends a redirect message to the client.
        """
        await self.send(
            text_data=json.dumps({"type": "redirect_tournament", "redirect": url})
        )

    async def send_winner(self, event: GameStateEvent) -> None:
        """
        Receives the game state from the worker and sends the winner to the client.

        Args:
            event (GameStateEvent): The event data containing the game state.
        """
        await self.define_winner(event)
        if self.winner:
            logger.info(f"Winner: {self.winner}")
            try:
                await self.send(
                    text_data=json.dumps({"type": "tournament_match_winner", "winner": self.winner})
                )
            except Exception as e:
                await self.send_error("Failed to send winner to client.")
                logger.exception(f"Failed to send winner to client: {e}")