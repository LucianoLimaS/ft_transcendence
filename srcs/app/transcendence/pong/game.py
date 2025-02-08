import random
import asyncio
from typing import Dict, Optional, TypedDict

THICKNESS = 10
BALL_SPEED = 4
MAX_SPEED = 10
PADDLE_SPEED = 7
WINNER_SCORE = 3
WIDTH, HEIGHT = 800, 400  # Dimensões do jogo


class BallPosition(TypedDict):
    x: float
    y: float
    size: float
    x_speed: float
    y_speed: float


class PaddlePosition(TypedDict):
    x: float
    y: float
    width: float
    height: float


class GameState(TypedDict):
    ball: BallPosition
    paddle_left: PaddlePosition
    paddle_right: PaddlePosition
    score: Dict[str, int]
    winner: Optional[str]


class Ball:
    def __init__(self) -> None:
        self.size = 10
        self.reset()

    def move(self) -> None:
        self.x += self.x_speed
        self.y += self.y_speed

    def bounce(self, axis: str) -> None:
        if axis == "x":
            self.x_speed = -self.x_speed * 1.1  # Aceleração a cada batida
            if abs(self.x_speed) > MAX_SPEED:
                self.x_speed = MAX_SPEED * (1 if self.x_speed > 0 else -1)
        elif axis == "y":
            self.y_speed = -self.y_speed

    def reset(self) -> None:
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.x_speed = random.choice([-BALL_SPEED, BALL_SPEED])
        self.y_speed = random.choice([-BALL_SPEED, BALL_SPEED])


class Paddle:
    def __init__(self, x: float) -> None:
        self.width = 10
        self.height = 80
        self.x = x
        self.y = HEIGHT / 2 - self.height / 2
        self.speed = 0

    def move(self) -> None:
        self.y += self.speed
        self.y = max(0, min(self.y, HEIGHT - self.height))  # Impede sair da tela


class PongGame:
    def __init__(self, singleplayer: bool, dificulty:int) -> None:
        self.ball = Ball()
        self.paddle_left = Paddle(10)
        self.paddle_right = Paddle(WIDTH - 20)
        self.score = {"left": 0, "right": 0}
        self.winner = None
        self.singleplayer = singleplayer
        self.dificulty = dificulty

    def move_ai(self) -> None:
        if self.ball.x_speed > 0:  # A IA só se move quando a bola vem para o lado dela
            if self.ball.y > self.paddle_right.y + self.paddle_right.height / 2:
                self.paddle_right.y += min(PADDLE_SPEED, HEIGHT - self.paddle_right.y - self.paddle_right.height)
            elif self.ball.y < self.paddle_right.y + self.paddle_right.height / 2:
                self.paddle_right.y -= min(PADDLE_SPEED, self.paddle_right.y)
        #colocar tempo 1000
        #fazer 3 niveis

    def check_collisions(self) -> None:
        # Colisão com o topo e a base
        if self.ball.y - self.ball.size <= 0 or self.ball.y + self.ball.size >= HEIGHT:
            self.ball.bounce("y")

        # Colisão com a raquete esquerda
        if (
            self.ball.x - self.ball.size <= self.paddle_left.x + self.paddle_left.width
            and self.paddle_left.y <= self.ball.y <= self.paddle_left.y + self.paddle_left.height
        ):
            self.ball.bounce("x")

        # Colisão com a raquete direita
        if (
            self.ball.x + self.ball.size >= self.paddle_right.x
            and self.paddle_right.y <= self.ball.y <= self.paddle_right.y + self.paddle_right.height
        ):
            self.ball.bounce("x")

        # Pontuação
        if self.ball.x - self.ball.size <= 0:
            self.score["right"] += 1
            self.ball.reset()
        elif self.ball.x + self.ball.size >= WIDTH:
            self.score["left"] += 1
            self.ball.reset()

        # Verifica se há um vencedor
        if self.score["left"] >= WINNER_SCORE:
            self.winner = "left"
        elif self.score["right"] >= WINNER_SCORE:
            self.winner = "right"
    
    def paddle_on(self, paddle: str, direction: str) -> None:
        """Ativa o movimento de uma paddle (para cima ou para baixo)."""
        if paddle == "left":
            if direction == "up":
                self.paddle_left.speed = -PADDLE_SPEED
            elif direction == "down":
                self.paddle_left.speed = PADDLE_SPEED
        elif paddle == "right":
            if direction == "up":
                self.paddle_right.speed = -PADDLE_SPEED
            elif direction == "down":
                self.paddle_right.speed = PADDLE_SPEED

    def paddle_off(self, paddle: str) -> None:
        """Desativa o movimento de uma paddle (para que ela pare)."""
        if paddle == "left":
            self.paddle_left.speed = 0
        elif paddle == "right":
            self.paddle_right.speed = 0

    async def game_tick(self) -> GameState:
        if self.winner:
            return await self.get_game_state()
        
        self.paddle_left.move()
        if self.singleplayer:
            self.move_ai()
        self.paddle_right.move()
        self.ball.move()
        self.check_collisions()
        
        return await self.get_game_state()

    async def get_game_state(self) -> GameState:
        return {
            "ball": {
                "x": self.ball.x,
                "y": self.ball.y,
                "size": self.ball.size,
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
