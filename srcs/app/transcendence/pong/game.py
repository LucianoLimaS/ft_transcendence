import random
import time
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
    def __init__(self, singleplayer: bool, difficulty: str = "normal") -> None:
        self.ball = Ball()
        self.paddle_left = Paddle(10)
        self.paddle_right = Paddle(WIDTH - 20)
        self.score = {"left": 0, "right": 0}
        self.winner = None
        self.singleplayer = singleplayer
        self.difficulty = difficulty
        self.last_ai_move_time = time.time()

    def predict_ball_position(self) -> float:
        estimated_y = self.ball.y
        ball_x = self.ball.x
        ball_y_speed = self.ball.y_speed

        while ball_x < WIDTH - self.paddle_right.width:
            estimated_y += ball_y_speed
            if estimated_y <= 0 or estimated_y >= HEIGHT:
                ball_y_speed *= -1
            ball_x += self.ball.x_speed

        return max(0, min(estimated_y, HEIGHT))

    def move_ai(self) -> None:
        """Movimenta a IA com base na dificuldade e direção da bola."""
        if self.ball.x_speed < 0:  # A bola está indo para a esquerda, IA não se move
            return

        center_y = self.paddle_right.y + self.paddle_right.height / 2

        if self.difficulty == "easy":
            if self.ball.y > center_y + 20:
                self.paddle_right.y = min(self.paddle_right.y + PADDLE_SPEED // 2, HEIGHT - self.paddle_right.height)
            elif self.ball.y < center_y - 20:
                self.paddle_right.y = max(self.paddle_right.y - PADDLE_SPEED // 2, 0)

        elif self.difficulty == "normal":
            if time.time() - self.last_ai_move_time < 0.05:  # Pequeno atraso
                return
            self.last_ai_move_time = time.time()

            error_factor = random.uniform(-5, 5)  # Introduz um pequeno erro na precisão
            target_y = self.ball.y + error_factor

            if abs(target_y - center_y) > 10:  # Tolerância para evitar tremores
                if target_y > center_y:
                    self.paddle_right.y = min(self.paddle_right.y + PADDLE_SPEED - 1, HEIGHT - self.paddle_right.height)
                else:
                    self.paddle_right.y = max(self.paddle_right.y - PADDLE_SPEED + 1, 0)

        elif self.difficulty == "hard":
            predicted_y = self.predict_ball_position()

            if abs(predicted_y - center_y) > 5:  # Se a diferença for menor que 5px, não se move
                if predicted_y > center_y:
                    self.paddle_right.y = min(self.paddle_right.y + int(PADDLE_SPEED * 1.2), HEIGHT - self.paddle_right.height)
                elif predicted_y < center_y:
                    self.paddle_right.y = max(self.paddle_right.y - int(PADDLE_SPEED * 1.2), 0)

    def check_collisions(self) -> None:
        # Colisão com a parede superior e inferior
        if self.ball.y - self.ball.size <= 0 or self.ball.y + self.ball.size >= HEIGHT:
            self.ball.bounce("y")

        # Colisão com o paddle esquerdo (considerando apenas a borda esquerda da bola)
        if (
            self.ball.x - self.ball.size <= self.paddle_left.x + self.paddle_left.width - 10
            and self.paddle_left.y <= self.ball.y <= self.paddle_left.y + self.paddle_left.height
            and self.ball.x_speed < 0
        ):
            self.ball.bounce("x")

        # Colisão com o paddle direito
        if (
            self.ball.x + self.ball.size >= self.paddle_right.x
            and self.paddle_right.y <= self.ball.y <= self.paddle_right.y + self.paddle_right.height
            and self.ball.x_speed > 0
        ):
            self.ball.bounce("x")

        # Atualiza o placar
        if self.ball.x - self.ball.size <= 0:  # A bola passou pelo paddle esquerdo
            self.score["right"] += 1
            self.ball.reset()
        elif self.ball.x + self.ball.size >= WIDTH:  # A bola passou pelo paddle direito
            self.score["left"] += 1
            self.ball.reset()

        # Verifica se algum jogador ganhou
        if self.score["left"] >= WINNER_SCORE:
            self.winner = "left"
        elif self.score["right"] >= WINNER_SCORE:
            self.winner = "right"

    def paddle_on(self, paddle: str, direction: str) -> None:
        if paddle == "left":
            if direction == "up":
                self.paddle_left.speed = -PADDLE_SPEED
            elif direction == "down":
                self.paddle_left.speed = PADDLE_SPEED
        elif paddle == "right" and not self.singleplayer:
            if direction == "up":
                self.paddle_right.speed = -PADDLE_SPEED
            elif direction == "down":
                self.paddle_right.speed = PADDLE_SPEED

    def paddle_off(self, paddle: str) -> None:
        if paddle == "left":
            self.paddle_left.speed = 0
        elif paddle == "right" and not self.singleplayer:
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
            "ball": self.ball.__dict__,
            "paddle_left": self.paddle_left.__dict__,
            "paddle_right": self.paddle_right.__dict__,
            "score": self.score,
            "winner": self.winner,
        }
