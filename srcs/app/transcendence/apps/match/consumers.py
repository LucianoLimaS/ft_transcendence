import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import random

active_games = {}  # Estrutura fora da classe para armazenar jogos ativos
game_states = {}   # Dicionário para armazenar o estado de cada jogo

class PongConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        await self.accept()
        self.game_id = None
        self.player_num = None
        await self.channel_layer.group_add("pong_lobby", self.channel_name)
        print(f"{self.user.username} Connected: {self.channel_name}")
        await self.send_json({"type": "waiting_for_player"}) # Envia a mensagem inicial

    async def receive_json(self, content):
        action = content.get("action")

        if action == "join_game":
            await self.join_game()
        elif action == "update_game_state":
            if self.game_id and self.player_num is not None:
                await self.update_game_state(content)
        elif action == "leave_game":
            await self.leave_game()

    async def join_game(self):
        for game_id, players in active_games.items():
            if len(players) == 1:
                self.game_id = game_id
                self.player_num = 2
                active_games[game_id].append(self) # Armazena a instância do Consumer
                await self.channel_layer.group_add(f"game_{self.game_id}", self.channel_name)
                await self.channel_layer.group_discard("pong_lobby", self.channel_name)

                # Envia os nomes dos jogadores quando o segundo jogador entra
                player1 = active_games[self.game_id][0]
                player2 = self  # self é o segundo jogador
                await self.channel_layer.group_send(
                    f"game_{self.game_id}",
                    {
                        "type": "game_start",
                        "player1_name": player1.user.username,
                        "player2_name": player2.user.username,
                    }
                )
                # Remove a mensagem "Aguardando jogador" para ambos os jogadores
                await self.send_json({"type": "player_joined"})  # para o segundo jogador
                await player1.send_json({"type": "player_joined"})  # para o primeiro jogador
                return

        self.game_id = str(random.randint(1000, 9999))
        self.player_num = 1
        active_games[self.game_id] = [self] # Armazena a instância do Consumer
        await self.channel_layer.group_add(f"game_{self.game_id}", self.channel_name)
        await self.channel_layer.group_discard("pong_lobby", self.channel_name)


    async def update_game_state(self, data):
        if self.game_id not in game_states:
            game_states[self.game_id] = {  # Inicializa o estado do jogo
                "ball_x": 400,
                "ball_y": 200,
                "ball_speed_x": 5,
                "ball_speed_y": 5,
                "left_paddle_y": 150,
                "right_paddle_y": 150,
                "left_score": 0,
                "right_score": 0,
            }

        game_state = game_states[self.game_id]  # Obtém o estado do jogo atual

        if self.player_num == 1:
            game_state["left_paddle_y"] = data["left_paddle_y"]
        elif self.player_num == 2:
            game_state["right_paddle_y"] = data["right_paddle_y"]


        # --- Lógica do Jogo (Colisões, Movimento da Bola, Pontuação) ---
        ball_x = game_state.get("ball_x", 400)
        ball_y = game_state.get("ball_y", 200)
        ball_speed_x = game_state.get("ball_speed_x", 5)
        ball_speed_y = game_state.get("ball_speed_y", 5)
        left_paddle_y = game_state.get("left_paddle_y", 150)
        right_paddle_y = game_state.get("right_paddle_y", 150)
        left_score = game_state.get("left_score", 0)
        right_score = game_state.get("right_score", 0)
        ball_radius = 10
        paddle_height = 100
        paddle_width = 10
        canvas_width = 800
        canvas_height = 400

        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Colisão com as paredes superior e inferior
        if ball_y + ball_radius > canvas_height or ball_y - ball_radius < 0:
            ball_speed_y = -ball_speed_y

        # Colisão com as pás
        if (
            ball_x - ball_radius < paddle_width and ball_y > left_paddle_y and ball_y < left_paddle_y + paddle_height
        ) or (
            ball_x + ball_radius > canvas_width - paddle_width and ball_y > right_paddle_y and ball_y < right_paddle_y + paddle_height
        ):
            ball_speed_x = -ball_speed_x

        # Pontuação
        if ball_x + ball_radius > canvas_width:
            left_score += 1
            ball_x = canvas_width / 2
            ball_y = random.randint(ball_radius, canvas_height - ball_radius)  # Posição Y aleatória ao reiniciar
            ball_speed_x = -5
            ball_speed_y = 5 if random.random() > 0.5 else -5

        elif ball_x - ball_radius < 0:
            right_score += 1
            ball_x = canvas_width / 2
            ball_y = random.randint(ball_radius, canvas_height - ball_radius) # Posição Y aleatória ao reiniciar
            ball_speed_x = 5
            ball_speed_y = 5 if random.random() > 0.5 else -5

        game_state.update({
            "ball_x": ball_x,
            "ball_y": ball_y,
            "ball_speed_x": ball_speed_x,
            "ball_speed_y": ball_speed_y,
            "left_score": left_score,
            "right_score": right_score,
        })

        # Atualiza game_states diretamente
        game_states[self.game_id] = game_state


        # Envia o estado *completo* do jogo
        await self.channel_layer.group_send(
            f"game_{self.game_id}",
            {
                "type": "game_state_update",
                **game_state, # Envia todo o game_state
            }
        )

    async def game_state_update(self, event):
        await self.send_json(event) # Envia o evento como JSON

    async def game_start(self, event):
        await self.send(text_data=json.dumps(
            {
                "type": "game_start",
                "player1_name": event["player1_name"],
                "player2_name": event["player2_name"],
                "player_num": self.player_num # Mantém o número do jogador para uso futuro
            }
        ))

    async def leave_game(self):
        if self.game_id:
            await self.channel_layer.group_discard(f"game_{self.game_id}", self.channel_name) # await diretamente
            self.game_id = None
            self.player_num = None

    async def disconnect(self, close_code):
        await self.leave_game()
        await self.channel_layer.group_discard("pong_lobby", self.channel_name) # await diretamente