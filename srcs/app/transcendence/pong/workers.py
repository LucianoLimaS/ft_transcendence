import asyncio
import logging
from dataclasses import dataclass
from typing import Dict, Optional

from channels.consumer import AsyncConsumer

from .game import PongGame  # Garantir que isso seja o caminho correto

logger = logging.getLogger(__name__)

@dataclass
class GameSession:
    """
    Represents a game session with its game instance and associated task.
    """
    game: PongGame
    task: Optional[asyncio.Task] = None

class PongGameWorker(AsyncConsumer):
    """
    Worker that handles the game logic and communication with the websocket group
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the worker with empty dictionaries to store game sessions.
        """
        super().__init__(*args, **kwargs)
        self.sessions: Dict[str, GameSession] = {}

    async def initialize_game(self, message: dict) -> None:
        """
        Initializes a new game session and sends the initial game state to the clients.

        Args:
            message (dict): The message containing initialization parameters.
        """
        try:
            room_id: str = message["room_id"]
            room_group_name: str = message["room_group_name"]
            width: int = message["width"]
            height: int = message["height"]

            if room_id not in self.sessions:
                game = PongGame(singleplayer=False)
                self.sessions[room_id] = GameSession(game=game)
                logger.info(f"Game initialized for room {room_id}")

            game_state = await self.sessions[room_id].game.get_game_state()

            await self.channel_layer.group_send(
                room_group_name,
                {
                    "type": "send_game_state",
                    "game_state": game_state,
                },
            )
        except Exception as e:
            logger.exception(f"Failed to initialize game: {e}")

    async def start_game_loop(self, room_id: str, room_group_name: str) -> None:
        """
        Runs the game loop, updating the game state and sending it to clients.

        Args:
            room_id (str): The ID of the room.
            room_group_name (str): The name of the room group.
        """
        try:
            session: Optional[GameSession] = self.sessions.get(room_id)
            if not session:
                logger.warning(f"No game session found for room {room_id}")
                return

            while room_id in self.sessions:
                game_state = await session.game.game_tick()
                logger.debug(f"Game state for room {room_id}: {game_state}")

                await self.channel_layer.group_send(
                    room_group_name,
                    {
                        "type": "send_game_state",
                        "game_state": game_state,
                    },
                )

                if session.game.winner:
                    await self.channel_layer.group_send(
                        room_group_name,
                        {
                            "type": "send_winner",
                            "game_state": game_state,
                        },
                    )
                    await self.cleanup_game(room_id)
                    break  # Exit the loop since the game has ended

                await asyncio.sleep(0.016)
        except Exception as e:
            logger.exception(f"Error in game loop for room {room_id}: {e}")
            await self.cleanup_game(room_id)

    async def start_game(self, message: dict) -> None:
        """
        Starts the game loop if not already started.

        Args:
            message (dict): The message containing room information.
        """
        try:
            room_id: str = message["room_id"]
            room_group_name: str = message["room_group_name"]

            if room_id not in self.sessions:
                await self.initialize_game(message)

            session: Optional[GameSession] = self.sessions.get(room_id)
            if not session:
                logger.warning(f"No game session found for room {room_id}")
                return

            if not session.task or session.task.done():
                session.task = asyncio.create_task(
                    self.start_game_loop(room_id, room_group_name)
                )
        except Exception as e:
            logger.exception(f"Failed to update game state for room {room_id}: {e}")

    async def update_paddles_position(self, message: dict) -> None:
        """
        Updates the paddle positions based on user input.

        Args:
            message (dict): The message containing paddle movement information.
        """
        try:
            room_id: str = message["room_id"]
            paddle: str = message["paddle"]
            direction: str = message["direction"]
            state: bool = message["state"]

            session: Optional[GameSession] = self.sessions.get(room_id)
            if not session:
                logger.warning(f"No session found for room {room_id}")
                return

            if session.game is None:
                logger.warning(f"Game object is None for room {room_id}")
                return

            if hasattr(session.game.paddle_on, '__call__') and asyncio.iscoroutinefunction(session.game.paddle_on):
                if state:
                    await session.game.paddle_on(paddle, direction)
                else:
                    await session.game.paddle_off(paddle)
            else:
                if state:
                    session.game.paddle_on(paddle, direction)  # Sem await
                else:
                    session.game.paddle_off(paddle)  # Sem await

        except Exception as e:
            logger.exception(
                f"Failed to update paddle positions for room {room_id}: {e}"
            )

    async def finish_game(self, message: dict) -> None:
        """
        Cleans up the game and task when the game ends.

        Args:
            message (dict): The message containing room information.
        """
        try:
            room_id: str = message["room_id"]
            await self.cleanup_game(room_id)
            logger.info(f"Game finished and cleaned up for room {room_id}")
        except Exception as e:
            logger.exception(f"Failed to finish game for room {room_id}: {e}")

    async def cleanup_game(self, room_id: str) -> None:
        """
        Cleans up game sessions for a room.

        Args:
            room_id (str): The ID of the room to clean up.
        """
        try:
            session: Optional[GameSession] = self.sessions.get(room_id)
            if session:
                if session.task and not session.task.cancelled():
                    session.task.cancel()
                    logger.info(f"Game task cancelled for room {room_id}")
                del self.sessions[room_id]
                logger.info(f"Game session deleted for room {room_id}")
            else:
                logger.warning(f"No game session to clean up for room {room_id}")
        except Exception as e:
            logger.exception(f"Failed to clean up game for room {room_id}: {e}")
