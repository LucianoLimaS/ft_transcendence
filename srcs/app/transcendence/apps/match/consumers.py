import json
from channels.generic.websocket import AsyncWebsocketConsumer
import random

class PongConsumer(AsyncWebsocketConsumer):
    # async def connect(self):
    #     await self.accept()
    #     self.game_id = None  # Inicialmente, nenhum jogo atribuído
    #     self.player_num = None
    #     await self.channel_layer.group_add("pong_lobby", self.channel_name) # Adiciona o consumer ao grupo de lobby
    async def connect(self):
        try:
            await self.accept()
            self.game_id = None
            self.player_num = None
            await self.channel_layer.group_add("pong_lobby", self.channel_name)
            print(f"Connected: {self.channel_name}")  # Log de depuração
        except Exception as e:
            print(f"Error in connect: {e}")  # Log de erro

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get("action")

        if action == "join_game":
            await self.join_game()
        elif action == "update_game_state":
             # Certifica-se de que o jogador está em um jogo antes de atualizar
            if self.game_id and self.player_num is not None:
                await self.update_game_state(data)
        elif action == "leave_game":
            await self.leave_game()


    async def join_game(self):
        # Lógica simplificada para encontrar/criar um jogo (apenas cria um novo por enquanto)
        # Em um cenário real, você precisaria de um sistema de matchmaking

        # Procura por um jogo com apenas um jogador no grupo "pong_lobby"
        for group_name in self.channel_layer.groups.keys():
            if group_name.startswith("game_") and len(self.channel_layer.groups[group_name]) == 1:
                self.game_id = group_name.split("_")[1]
                self.player_num = 2
                await self.channel_layer.group_add(f"game_{self.game_id}", self.channel_name)
                await self.channel_layer.group_discard("pong_lobby", self.channel_name)  # Remove do lobby
                # Notifica os jogadores que o jogo começou
                await self.channel_layer.group_send(
                    f"game_{self.game_id}",
                    {
                        "type": "game_start",
                    }
                )

                return

        # Se nenhum jogo encontrado, cria um novo
        self.game_id = str(random.randint(1000, 9999))  # Gera um ID de jogo aleatório
        self.player_num = 1
        await self.channel_layer.group_add(f"game_{self.game_id}", self.channel_name)
        await self.channel_layer.group_discard("pong_lobby", self.channel_name) # Remove do lobby



    async def update_game_state(self, data):
        # Obtem o estado atual do jogo (se existir)
        game_state = self.channel_layer.groups.get(f"game_{self.game_id}", {}).get("game_state", {})

        # Define a posição das pás com base nos dados recebidos do cliente
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

        # Atualiza o estado do jogo
        game_state["ball_x"] = ball_x
        game_state["ball_y"] = ball_y
        game_state["ball_speed_x"] = ball_speed_x
        game_state["ball_speed_y"] = ball_speed_y
        game_state["left_score"] = left_score
        game_state["right_score"] = right_score


        # Salva o estado do jogo no grupo
        self.channel_layer.groups[f"game_{self.game_id}"]["game_state"] = game_state


        # Envia o estado do jogo para ambos os jogadores
        await self.channel_layer.group_send(
            f"game_{self.game_id}",
            {
                "type": "game_state_update",
                "ball_x": ball_x,
                "ball_y": ball_y,
                "left_paddle_y": left_paddle_y,
                "right_paddle_y": right_paddle_y,
                "left_score": left_score,
                "right_score": right_score,
            }
        )



    async def game_state_update(self, event):
         # Envia o estado do jogo para o cliente
        await self.send(text_data=json.dumps(event))


    async def game_start(self, event):
        await self.send(text_data=json.dumps({"type": "game_start"}))



    async def leave_game(self):
        if self.game_id:
            await self.channel_layer.group_discard(f"game_{self.game_id}", self.channel_name)
            self.game_id = None
            self.player_num = None


    async def disconnect(self, close_code):

        await self.leave_game() # Garante que o jogador saia do jogo ao desconectar
        await self.channel_layer.group_discard("pong_lobby", self.channel_name) # Remove do lobby ao desconectar