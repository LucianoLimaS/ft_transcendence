import asyncio
from django.core.cache import cache

from typing import Optional

from .base_consumer import (
    BasePongConsumer,
    ClientMessage,
    Direction,
    GameStateEvent,
    Paddle,
    logger,
)


class LocalPongConsumer(BasePongConsumer):
    """
    LocalPongConsumer handles the game logic for local (single-player) games.
    Inherits from BasePongConsumer.
    """

    async def connect(self) -> None:
        """
        Handles the WebSocket connection event.
        Initializes local game-specific variables..
        """
        await super().connect()

        # Initialize variables that will be used after join_room
        self.current_player_id: Optional[int] = None
        self.ready_lock = asyncio.Lock()

    async def handle_join_room(self, data: ClientMessage) -> None:
        """
        Handles the 'join_room' message from the client.

        Args:
            data (ClientMessage): The data received from the client.
        """
        try:
            self.room_id = data["room_id"]
            await self.add_to_group(self.room_id)

            async with self.ready_lock:
                self.current_player_id = cache.get(
                    f"{self.room_group_name}_current_player_id", None
                )

                # Check if the room is active and not occupied
                room = await self.get_room_by_id(self.room_id)
                if not room.is_active:
                    await self.send_alert_message("Room is inactive.")
                    logger.info(f"User {self.scope['user']} attempted to join an inactive room {self.room_id}.")
                    if self.room_group_name:
                        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
                    await self.close()
                    return

                if self.current_player_id:
                    await self.send_alert_message({"message":"Room is already occupied."})
                    logger.info(f"User {self.scope['user']} attempted to join an occupied room {self.room_id}.")
                    if self.room_group_name:
                        # Remove the user from the group
                        await self.channel_layer.group_discard(
                            self.room_group_name, self.channel_name
                        )
                    await self.close()
                    
                else:
                    self.current_player_id = self.scope['user'].id
                    cache.set(f"{self.room_group_name}_current_player_id", self.current_player_id)

                    await self.initialize_game_data(data["width"], data["height"])
                    await self.worker_initialize_game()
                    logger.info(f"User {self.scope['user']} joined.")
        except Exception as e:
            await self.send_error("Failed to join room.")
            logger.exception(f"Failed to handle join_room: {e}")

    async def start_game(self) -> bool:
        """
        Starts the game. In local mode, the game starts immediately upon receiving the 'start_game' message
        """
        try:
            await self.worker_start_game()
            return True
        except Exception as e:
            await self.send_error("Failed to start game.")
            logger.exception(f"Failed to start game: {e}")
        return False

    async def handle_key_paddle_event(self, key: str, state: bool) -> None:
        """
        Handles key events from the client for moving paddles.
        In local mode, `w` and `s` keys are used to move the left paddle, and `arrowup` and `arrowdown` keys are used to move the right paddle.

        Args:
            key (str): The key that was pressed or released.
            state (bool): True if the key is pressed, False if it is released.
        """
        try:
            if key in ["w", "s"]:
                paddle = Paddle.LEFT
                direction = Direction.UP if key == "w" else Direction.DOWN
            elif key in ["arrowup", "arrowdown"]:
                paddle = Paddle.RIGHT
                direction = Direction.UP if key == "arrowup" else Direction.DOWN
            else:
                logger.warning(f"Unhandled key: {key}")
                return

            await self.worker_update_paddles_position(paddle, direction, state)
        except Exception as e:
            await self.send_error("Failed to handle key event.")
            logger.exception(f"Failed to handle key_paddle_event: {e}")

    async def finish_game(self) -> None:
        """
        Finishes the game. In local mode, the game is finished when the user closes the browser window.
        Performs any necessary cleanup operations.
        """
        try:
            async with self.ready_lock:
                if self.current_player_id == self.scope['user'].id:
                    # Send a message to the worker to finish the game
                    await self.channel_layer.send(
                        "pong_update_channel",
                        {
                            "type": "finish_game",
                            "room_id": str(self.room_id),
                        },
                    )

                    # Delete game data
                    cache.delete(f"{self.room_group_name}_game_data")
                    cache.delete(f"{self.room_group_name}_current_player_id")
                    # Set room inactive
                    await self.set_room_inactive()
                    logger.info(
                        f"Game finished and cleaned up for room {self.room_group_name}"
                    )

            if self.room_group_name:
                # Remove the user from the group
                await self.channel_layer.group_discard(
                    self.room_group_name, self.channel_name
                )

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
            game_state = event["game_state"]
            self.winner = game_state["winner"]
        except Exception as e:
            await self.send_error("Failed to define winner.")
            logger.exception(f"Failed to define winner: {e}")
