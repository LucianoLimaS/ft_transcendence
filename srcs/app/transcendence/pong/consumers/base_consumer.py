import json
import logging
from enum import Enum
from typing import Dict, Optional, TypedDict, Union

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
from pong.game import GameState
from pong.models import PongRoom

logger = logging.getLogger(__name__)


class Paddle(str, Enum):
    LEFT = "left"
    RIGHT = "right"


class Direction(str, Enum):
    UP = "up"
    DOWN = "down"


class MessageType(str, Enum):
    JOIN_ROOM = "join_room"
    START_GAME = "start_game"
    KEYDOWN = "keydown"
    KEYUP = "keyup"


class ClientMessageRequired(TypedDict):
    type: MessageType


class ClientMessage(ClientMessageRequired, total=False):
    room_id: int
    width: int
    height: int
    key: str


class StartGameEvent(TypedDict):
    type: str
    message: str


class GameStateEvent(TypedDict):
    type: str
    game_state: GameState


class BasePongConsumer(AsyncWebsocketConsumer):
    """
    Base consumer for the Pong game.
    Manages WebSocket connections and communication with the game worker.
    Subclasses should implement game-specific logic.
    """

    async def connect(self) -> None:
        """
        Handles the WebSocket connection event.
        Only authenticated users can connect. Otherwise, the connection is closed.
        Initializes game data and accepts the connection.
        """
        try:
            if self.scope["user"].is_anonymous:
                await self.accept()
                await self.send(
                    text_data=json.dumps(
                        {"type": "not_auth", "message": "User not authenticated"}
                    )
                )
                await self.close()
            else:
                self.room_id: Optional[int] = None
                self.room_group_name: Optional[str] = None
                self.game_data: Dict[str, Union[int, float]] = {}
                self.winner: Optional[str] = None
                await self.accept()
        except Exception as e:
            logger.exception(f"Error during connection: {e}")
            try:
                await self.send_error("An error during connection occurred.")
            finally:
                await self.close()

    async def disconnect(self, close_code: int) -> None:
        """
        Handles the WebSocket disconnection event.
        Calls the finish_game method to perform any necessary cleanup.
        """
        try:
            await self.finish_game()
        except Exception as e:
            logger.exception(f"Error during disconnection: {e}")

    async def receive(self, text_data: str) -> None:
        """
        Receives messages from the Websocket client and routes them to appropriate handlers.

        Args:
            text_data (str): The JSON string received from the WebSocket client.
        """
        try:
            data_json: ClientMessage = json.loads(text_data)
            message_type: MessageType = data_json["type"]

            if message_type == MessageType.JOIN_ROOM:
                await self.handle_join_room(data_json)
            elif message_type == MessageType.START_GAME:
                await self.handle_start_game()
            elif message_type in [MessageType.KEYDOWN, MessageType.KEYUP]:
                key: Optional[str] = data_json["key"]
                if key is None:
                    await self.send_error("Key not provided")
                    logger.warning(f"Missing 'key' in message: {data_json}")
                    return
                state: bool = (
                    message_type == MessageType.KEYDOWN
                )  # True if 'keydown', False if 'keyup'
                await self.handle_key_paddle_event(key, state)
            else:
                await self.send_error("Received an unknown message type.")
                logger.warning(f"Unknown message type received: {message_type}")
        except json.JSONDecodeError:
            await self.send_error("Invalid JSON data")
            logger.exception("JSON decoding failed.")
        except Exception as e:
            await self.send_error("An unexpected error occurred.")
            logger.exception(f"An error occurred: {e}")

    # Methods to interact with the database
    @sync_to_async
    def get_room_by_id(self, room_id: int) -> PongRoom:
        """
        Retrieves a PongRoom by ID.

        Args:
            room_id (int): The ID of the PongRoom.

        Returns:
            PongRoom: The PongRoom object corresponding to the room ID.
        """
        return PongRoom.objects.select_related("tournament").get(id=room_id)

    @sync_to_async
    def mark_room_as_inactive(self, room):
        """
        Marks the room as inactive in the database.
        """
        room.is_active = False
        room.save()

    async def set_room_inactive(self) -> None:
        """
        Get and sets the room as inactive in the database.
        """
        try:
            pongroom = await self.get_room_by_id(self.room_id)
            await self.mark_room_as_inactive(pongroom)
            logger.info(f"Room {self.room_id} set to inactive")
        except Exception as e:
            logger.exception(f"Failed to set room inactive: {e}")

    # main methods - game state
    async def add_to_group(self, room_id: int) -> None:
        """
        Adds the consumer to the appropriate group based on the room ID.

        Args:
            room_id (int): The ID of the room to join.
        """
        try:
            self.room_id = room_id
            self.room_group_name = f"pong_{self.room_id}"
            cached_data = cache.get(f"{self.room_group_name}_game_data")
            if cached_data is not None:
                self.game_data = cached_data
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            logger.info(f"{self.scope['user']} added to group {self.room_group_name}")
        except Exception as e:
            await self.send_error("Failed to add to group.")
            logger.exception(f"Failed to add to group: {e}")

    async def initialize_game_data(self, width: int, height: int) -> None:
        """
        Initializes the game data with the provided width and height if not already set.

        Args:
            width (int): The width of the game area.
            height (int): The height of the game area.
        """
        try:
            if not self.game_data:
                self.game_data["width"] = width
                self.game_data["height"] = height
                cache.set(f"{self.room_group_name}_game_data", self.game_data)
                logger.info(f"Game data initialized: {self.game_data}")
        except Exception as e:
            await self.send_error("Failed to initialize game data.")
            logger.exception(f"Failed to initialize game data: {e}")

    async def handle_start_game(self) -> None:
        """
        Handles the `start_game` message from the client.
        Calls the `start_game` method and sends a message to the group indicate that game has started!
        """
        start_game = await self.start_game()
        if start_game:
            logger.info("Game started")
            if self.room_group_name:
                try:
                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            "type": "send_game_has_started_message",
                            "message": "Game started",
                        },
                    )
                except Exception as e:
                    await self.send_error("Failed to send start game message to group.")
                    logger.exception(f"Failed to send start game message: {e}")
            else:
                await self.send_error("Room group name not set")
                logger.warning(
                    "Room group name is not set when trying to start the game."
                )

    # Methods to send messages to the worker
    async def worker_initialize_game(self) -> None:
        """
        Sends a message to the worker to initialize the game. Its purpose is to draw the game without starting it.
        """
        try:
            await self.channel_layer.send(
                "pong_update_channel",
                {
                    "type": "initialize_game",
                    "room_id": str(self.room_id),
                    "room_group_name": self.room_group_name,
                    "width": self.game_data["width"],
                    "height": self.game_data["height"],
                },
            )
        except Exception as e:
            await self.send_error("Failed to initialize game in worker.")
            logger.exception(f"Failed to send initialize_game to worker: {e}")

    async def worker_start_game(self) -> None:
        """
        Sends a message to the worker to start the game loop.
        """
        try:
            await self.channel_layer.send(
                "pong_update_channel",
                {
                    "type": "start_game",
                    "room_id": str(self.room_id),
                    "room_group_name": self.room_group_name,
                    "width": self.game_data["width"],
                    "height": self.game_data["height"],
                },
            )
        except Exception as e:
            await self.send_error("Failed to start game in worker.")
            logger.exception(f"Failed to send update_game_state to worker: {e}")

    async def worker_update_paddles_position(
        self, paddle: Paddle, direction: Direction, state: bool
    ) -> None:
        """
        Sends a message to the worker to update the positions based on user input.

        Args:
            paddle (Paddle): The paddle to move (`left` or `right`).
            direction (Direction): The direction to move (`up` or `down`).
            state (bool): True if the key is pressed, False if it is released.
        """
        try:
            await self.channel_layer.send(
                "pong_update_channel",
                {
                    "type": "update_paddles_position",
                    "room_id": str(self.room_id),
                    "paddle": paddle,
                    "direction": direction,
                    "state": state,
                },
            )
        except Exception as e:
            await self.send_error("Failed to send update_paddles_position to worker.")
            logger.exception(f"Failed to send update_paddles_position to worker: {e}")

    # Methods to send messages to the client 
    async def send_game_has_started_message(self, event: StartGameEvent) -> None:
        """
        Sends a message to the client indicating that the game has started.

        Args:
            event (StartGameEvent): The event data containing the message.
        """
        try:
            await self.send(
                text_data=json.dumps(
                    {"type": "game_has_started", "message": event["message"]}
                )
            )
        except Exception as e:
            await self.send_error("Failed to send start game message to client.")
            logger.exception(f"Failed to send start game message to client: {e}")

    async def send_game_state(self, event: GameStateEvent) -> None:
        """
        Receives the game state from the worker and sends it to the client.

        Args:
            event (GameStateEvent): The event data containing the game state.
        """
        try:
            game_state = event["game_state"]
            await self.send(
                text_data=json.dumps({"type": "game_init", "game_state": game_state})
            )
        except Exception as e:
            await self.send_error("Failed to send game state to client.")
            logger.exception(f"Failed to send game state to client: {e}")

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
                    text_data=json.dumps({"type": "winner", "winner": self.winner})
                )
            except Exception as e:
                await self.send_error("Failed to send winner to client.")
                logger.exception(f"Failed to send winner to client: {e}")

    async def send_error(self, message: str) -> None:
        """
        Sends an error message to the client.

        Args:
            message (str): The error message to send.
        """
        await self.send(text_data=json.dumps({"type": "error", "message": message}))

    async def send_alert_message(self, event) -> None:
        """
        Send an alert message to the client.

        Args:
            message (str): Message to send alert erros.
        """
        await self.send(text_data=json.dumps({
                "type": "alert_message",
                "message": event["message"]
            })
        )

    # abstract methods
    async def handle_join_room(self, data: ClientMessage) -> None:
        """
        Handles the `join_room` message from the client.
        Should be implemented by subclasses.

        Args:
            data (ClientMessage): The data received from the client.
        """
        pass

    async def start_game(self) -> bool:
        """
        Should be implemented by subclasses.
        """
        pass

    async def handle_key_paddle_event(self, key: str, state: bool) -> None:
        """
        Handles key events from the client for moving paddles.
        Should be implemented by subclasses.

        Args:
            key (str): The key that was pressed or released.
            state (bool): True if the key is pressed, False if it is released.
        """
        pass

    async def finish_game(self) -> None:
        """
        Performs any necessary cleanup when the game ends.
        Should be implemented by subclasses.
        """
        pass

    async def define_winner(self, event: GameStateEvent) -> None:
        """
        Defines the winner.
        Should be implemented by subclasses.
        """
        pass
