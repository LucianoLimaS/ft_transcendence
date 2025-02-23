import asyncio
from typing import Dict, List, Optional

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from django.core.cache import cache
from pong.models import Match
from django.contrib.auth.models import User

from .base_consumer import (
    BasePongConsumer,
    ClientMessage,
    Direction,
    GameStateEvent,
    Paddle,
    logger,
)


class OnlinePongConsumer(BasePongConsumer):
    """
    OnlinePongConsumer handles the game logic for online (multiplayer) games.
    Inherits from BasePongConsumer.
    """

    async def connect(self) -> None:
        """
        Handles the WebSocket connection event.
        Initializes online game-specific variables.
        """
        await super().connect()
        self.player_paddle: Optional[str] = None
        self.is_ready: bool = False
        self.had_a_match: bool = False

        # Initialize variables that will be used after join_room
        self.ready_players: int = 0
        self.players_data: List[int] = []
        self.match_id: Optional[int] = None
        self.connected_players: Dict[int, bool] = {}

        self.ready_lock = asyncio.Lock()

        self.room_group_name = f"room_{self.scope['user'].username}"  # Exemplo de inicialização
        # players_data = cache.get(f"{self.room_group_name}_players", [])

    # Methods to interact with the database
    async def create_match(self) -> None:
        """
        Creates a new match record in the database.
        """
        try:
            players_data = cache.get(f"{self.room_group_name}_players", [])
            if players_data:
                player1 = await self.get_player_by_id(players_data[0])
                player2 = await self.get_player_by_id(players_data[1])
                pongroom = await self.get_room_by_id(self.room_id)

                match = await self.create_match_bd(player1, player2, pongroom)
                cache.set(f"{self.room_group_name}_match_id", match.id)
                logger.info(f"Match created: {match}")
        except Exception as e:
            await self.send_error("Failed to create match.")
            logger.exception(f"Failed to create match: {e}")

    @sync_to_async
    def get_player_by_id(self, player_id: int) -> User:
        """
        Retrieves a player (User) by ID.

        Args:
            player_id (int): The ID of the player.

        Returns:
            User (TrUser): The User object corresponding to the player ID.
        """
        return get_user_model().objects.get(id=player_id)

    @sync_to_async
    def create_match_bd(self, player1, player2, room):
        return Match.objects.create(room=room, player1=player1, player2=player2)

    @sync_to_async
    def get_match_by_id(self, match_id: int) -> Match:
        """
        Retrieves a Match by ID, selecting related player1 and player2.

        Args:
            match_id (int): The ID of the Match.

        Returns:
            Match: The Match object corresponding to the match ID.
        """
        return Match.objects.select_related("player1", "player2").get(id=match_id)

    @sync_to_async
    def set_match_winner(self, match, winner) -> None:
        """
        Sets the winner of a match.

        Args:
            match (Match): The Match object.
            winner (TrUser): The User object representing the winner.
        """
        match.winner = winner
        match.finished = True
        match.save()

    # abstract methods
    async def handle_join_room(self, data: ClientMessage) -> None:
        print("----    PASSEI AQUI    ----    [05]")
        """
        Handles the 'join_room' message from the client.

        Args:
            data (ClientMessage): The data received from the client.
        """
        try:
            self.room_id = data["room_id"]
            await self.add_to_group(self.room_id)

            # Now that self.room_group_name is initialized
            async with self.ready_lock:
                self.players_data = cache.get(f"{self.room_group_name}_players", [])
                self.connected_players = cache.get(
                    f"{self.room_group_name}_connected_players", {}
                )
                self.ready_players = cache.get(
                    f"{self.room_group_name}_ready_players", 0
                )
                self.match_id = cache.get(f"{self.room_group_name}_match_id", None)

                # Check if the room is active
                room = await self.get_room_by_id(self.room_id)
                if not room.is_active:
                    await self.send_alert_message({"message": "Room is inactive."})
                    logger.info(f"User {self.scope['user']} attempted to join an inactive room {self.room_id}.")
                    if self.room_group_name:
                        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
                    await self.close()
                    return
                
                # check if the room already has 2 players
                if len(self.players_data) >= 2 and self.scope["user"].id not in self.players_data:
                    await self.send_alert_message({"message": "Room is full."})
                    logger.info(f"User {self.scope['user']} attempted to join a full room {self.room_id}.")
                    if self.room_group_name:
                        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
                    await self.close()
                    return

                if self.scope["user"].id in self.players_data:
                    # User is reconnecting
                    self.connected_players[self.scope["user"].id] = True
                    index = self.players_data.index(self.scope["user"].id)
                    self.player_paddle = Paddle.LEFT if index == 0 else Paddle.RIGHT
                
                else:
                    # New player
                    self.player_paddle = (
                        Paddle.LEFT if not self.players_data else Paddle.RIGHT
                    )
                    self.players_data.append(self.scope["user"].id)
                    self.connected_players[self.scope["user"].id] = True
                    cache.set(f"{self.room_group_name}_players", self.players_data)

                cache.set(
                    f"{self.room_group_name}_connected_players", self.connected_players
                )

            await self.initialize_game_data(data["width"], data["height"])
            await self.worker_initialize_game()
        except Exception as e:
            await self.send_error("Failed to join room.")
            logger.exception(f"Failed to handle join_room: {e}")

    async def start_game(self) -> bool:
        """
        Starts the game when both players are ready.
        In online game mode, the game only starts when both players are ready, that is, they press play
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
                        self.match_id = cache.get(
                            f"{self.room_group_name}_match_id", None
                        )
                        self.had_a_match = cache.get(
                            f"{self.room_group_name}_had_a_match", False
                        )
                        self.had_a_match = True
                        self.had_a_match = cache.set(
                            f"{self.room_group_name}_had_a_match", self.had_a_match
                        )
                        if not self.match_id:
                            await self.worker_start_game()
                            await self.create_match()
                            return True
        except Exception as e:
            await self.send_error("Failed to start game.")
            logger.exception(f"Failed to start game: {e}")
        return False

    async def handle_key_paddle_event(self, key: str, state: bool) -> None:
        """
        Handles key events from the client for moving paddles.

        Args:
            key (str): The key that was pressed or released.
            state (bool): True if the key is pressed, False if it is released.
        """
        try:
            paddle = self.player_paddle
            if key in ["w", "arrowup"]:
                direction = Direction.UP
            elif key in ["s", "arrowdown"]:
                direction = Direction.DOWN
            else:
                logger.warning(f"Unhandled key: {key}")
                return

            await self.worker_update_paddles_position(paddle, direction, state)
        except Exception as e:
            await self.send_error("Failed to handle key event.")
            logger.exception(f"Failed to handle key_paddle_event: {e}")

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

    async def define_winner(self, event: GameStateEvent) -> None:
        """
        Defines the winner based on the game state received from the worker.

        Args:
            event (GameStateEvent): The event data containing the game state.
        """
        try:
            async with self.ready_lock:
                match_id = cache.get(f"{self.room_group_name}_match_id", None)
                if match_id:
                    match = await self.get_match_by_id(match_id)
                    if match.winner is None:
                        winner_side = event["game_state"]["winner"]
                        if winner_side == Paddle.LEFT:
                            match.winner = match.player1
                        else:
                            match.winner = match.player2
                        self.winner = match.winner.username
                        await self.set_match_winner(match, match.winner)
                        self.ready_players = 0
                        self.is_ready = False
                        self.match_id = None
                        cache.set(
                            f"{self.room_group_name}_ready_players",
                            self.ready_players,
                        )
                        cache.set(f"{self.room_group_name}_match_id", self.match_id)
                    else:
                        self.winner = None
        except Exception as e:
            await self.send_error("Failed to define winner.")
            logger.exception(f"Failed to define winner: {e}")

    # Online mode helper methods
