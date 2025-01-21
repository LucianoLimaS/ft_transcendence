import random
import asyncio
from typing import Dict, Optional, TypedDict

THICKNESS = float(15.0)
BALL_SPEED = float(5.0)
MAX_SPEED = float(12.0)
PADDLE_SPEED = float(BALL_SPEED * 2)
X = "x"
Y = "y"
RIGHT = "right"
LEFT = "left"
UP = "up"
DOWN = "down"
STOP = "stop"
WINNER_SCORE = 3

class BallPosition(TypedDict):
    x: float
    y: float
    size: float
    center: float
    x_speed: float
    y_speed: float


class PaddlePosition(TypedDict):
    x: float
    y: float
    width: float
    height: float


class GameState(TypedDict):
    width: int
    height: int
    ball: BallPosition
    paddle_left: PaddlePosition
    paddle_right: PaddlePosition
    players: Dict[str, str]
    score: Dict[str, int]
    winner: Optional[int]


class Ball:
    def __init__(self, width: int, height: int) -> None:
        """
        Ball class constructor. Initializes the ball's size, position, and speed.
        Self x and y coordinates are defined relative to the top-left corner.

        Args:
            width (int): The width of game are from canvas.
            height (int): The height of the game area from canvas.
        """
        self.size: float = float(THICKNESS)
        self.center: float = float(self.size / 2)
        self.base_speed: float = BALL_SPEED
        self.max_speed: float = MAX_SPEED
        self.x_start: float = float(width / 2) - self.center
        self.y_start: float = float(height / 2) - self.center
        self.y_min_start: int = 6 * THICKNESS
        self.y_max_start: int = height - (6 * THICKNESS)
        self.x: float = self.x_start
        self.y: float = self.y_start
        self.x_speed: float = float(self.base_speed)
        self.y_speed: float = float(self.base_speed)

    def move(self) -> None:
        """
        Updates the ball's position based on its current speed.
        """
        self.x += self.x_speed
        self.y += self.y_speed

    def bounce(self, direction: str) -> None:
        """
        Reverses the ball's speed in the given direction.

        Args:
            direction (str): The direction in which to reverse the ball's speed ('x' or 'y').
        """
        if direction == X:
            self.x_speed *= -1
            self.x_speed *= 1.1
            if self.x_speed > self.max_speed:
                self.x_speed = self.max_speed
        elif direction == Y:
            self.y_speed *= -1

    def reset(self) -> None:
        """
        Reset the ball to the center of the game area with a random y position and speed.
        """
        self.x = self.x_start
        self.y = float(random.randint(int(self.y_min_start), int(self.y_max_start)))
        self.x_speed = self.base_speed
        if random.randint(0, 1) == 0:
            self.bounce(X)
        angle = random.choice([0,1,2])
        if angle == 0:
            self.y_speed = 1.2 * self.base_speed
        elif angle == 1:
            self.y_speed = self.base_speed
        elif angle == 2:
            self.y_speed = 0.8 * self.base_speed


class Paddle:
    def __init__(self, width: int, height: int, side: str) -> None:
        """
        Paddle class constructor. Initializes the paddle's position, size, and movement speed.

        Args:
            width (int): The width of the game area.
            height (int): The height of the game area.
            side (str): The side the paddle is on ('left' or 'right').
        """
        self.width: float = float(THICKNESS)
        self.height: float = 120.0
        self.top_limit: float = float(THICKNESS)
        self.bottom_limit: float = float(height - self.height - THICKNESS)
        self.y: float = float(height / 2) - (self.height / 2)
        if side == LEFT:
            self.x: float = float(THICKNESS * 2)
        else:
            self.x: float = float(width - self.width - (THICKNESS * 2))
        self.speed: float = 0.0

    async def set_speed(self, direction: str) -> None:
        """
        Sets the paddle's speed based on the direction of movement.

        Args:
            direction (str): The direction to move the paddle ('up', 'down', or 'stop').
        """
        if direction == UP:
            self.speed = -PADDLE_SPEED
        elif direction == DOWN:
            self.speed = PADDLE_SPEED
        elif direction == STOP:
            self.speed = 0

    def limit(self) -> None:
        """
        Limits the paddle's movement to prevent it from moving outside the game area.
        """
        if self.y <= self.top_limit:
            self.y = self.top_limit

        if self.y >= self.bottom_limit:
            self.y = self.bottom_limit

    def move(self) -> None:
        """
        Updates the paddle's position based on its speed and applies movement limits.
        """
        self.y += self.speed
        self.limit()


class PongGame:
    def __init__(self, width: int, height: int) -> None:
        """
        PongGame class constructor. Initializes the game area, ball, and paddles.

        Args:
            width (int): The width of the game area.
            height (int): The height of the game area.
        """
        self.width: int = width
        self.height: int = height
        self.ball: Ball = Ball(width, height)
        self.paddle_left: Paddle = Paddle(width, height, LEFT)
        self.paddle_right: Paddle = Paddle(width, height, RIGHT)
        self.score: Dict[str, int] = {"left": 0, "right": 0}
        self.winner: Optional[str] = None
        self.lock: asyncio.Lock = asyncio.Lock()

    def update_score(self, side: str) -> None:
        """
        Updates the score for the given side and checks if a player has won.
        """
        self.score[side] += 1
        if self.score[side] == WINNER_SCORE:
            self.winner = side

    async def paddle_on(self, paddle: str, direction: str) -> None:
        """
        Activates the paddle's movement based on the key pressed.

        Args:
            paddle (str): The paddle to move ('left' or 'right').
            direction (str): The direction to move the paddle ('up' or 'down').
        """
        async with self.lock:
            if paddle == "left":
                await self.paddle_left.set_speed(direction)
            if paddle == "right":
                await self.paddle_right.set_speed(direction)

    async def paddle_off(self, paddle: str) -> None:
        """
        Stops the paddle's movement when the key is released.

        Args:
            paddle(str): The paddle to stop ('left' or 'right').
        """
        async with self.lock:
            if paddle == "left":
                await self.paddle_left.set_speed(STOP)
            elif paddle == "right":
                await self.paddle_right.set_speed(STOP)

    def calculate_ball_colision(self) -> None:
        """
        Checks if the ball hits the top or bottom boundaries and bounces it.
        Resets the ball if it hits the left or right boundaries.
        """
        if self.ball.y <= THICKNESS or self.ball.y + self.ball.size >= (
            self.height - THICKNESS
        ):
            self.ball.bounce(Y)
        if self.ball.x <= 0:
            self.update_score(RIGHT)
            self.ball.reset()
        if self.ball.x + self.ball.size >= self.width:
            self.update_score(LEFT)
            self.ball.reset()

    def calculate_paddle_colision(self) -> None:
        """
        Checks if the ball hits the paddles and bounces it.
        """
        if self.paddle_left.x <= self.ball.x <= self.paddle_left.x + self.paddle_left.width:
            if self.paddle_left.y <= self.ball.y <= self.paddle_left.y + self.paddle_left.height:
                self.ball.bounce(X)
                self.ball.x = self.paddle_left.x + self.paddle_left.width

        if self.paddle_right.x <= self.ball.x + self.ball.size <= self.paddle_right.x + self.paddle_right.width:
            if self.paddle_right.y <= self.ball.y <= self.paddle_right.y + self.paddle_right.height:
                self.ball.bounce(X)
                self.ball.x = self.paddle_right.x - self.ball.size


    def check_colisions(self) -> None:
        """
        Checks for collisions between the ball and the paddles.
        """
        self.calculate_ball_colision()
        self.calculate_paddle_colision()

    def move_objects(self) -> None:
        """
        Moves the ball and paddles based on their current speeds.
        """
        self.ball.move()
        self.paddle_left.move()
        self.paddle_right.move()

    async def calculate_game_tick(self) -> GameState:
        """
        Checks for collisions and moves the objects in the game if the game has no winner.
        Returns the current state of the game.
        """
        async with self.lock:
            self.check_colisions()
            # just do next move if the game is not finished, so don't have a winner
            if not self.has_winner():
                self.move_objects()
            return await self.get_game_state()

    def has_winner(self) -> bool:
        """
        Checks if a player has reached the winning score.
        """
        return bool(self.winner)

    async def get_game_state(self) -> GameState:
        """
        Returns the current state of the game.
        """
        return {
            "width": self.width,
            "height": self.height,
            "ball": {
                "x": self.ball.x,
                "y": self.ball.y,
                "size": self.ball.size,
                "center": self.ball.center,
                "x_speed": self.ball.x_speed,
                "y_speed": self.ball.y_speed,
            },
            "paddle_left": {
                "x": self.paddle_left.x,
                "y": self.paddle_left.y,
                "width": self.paddle_left.width,
                "height": self.paddle_left.height,
            },
            "paddle_right": {
                "x": self.paddle_right.x,
                "y": self.paddle_right.y,
                "width": self.paddle_right.width,
                "height": self.paddle_right.height,
            },
            "score": self.score,
            "winner": self.winner,
        }
