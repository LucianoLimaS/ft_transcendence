# srcs/app/transcendence/apps/chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.http import AsyncHttpConsumer
import logging

# Configure o logger
logging.basicConfig(level=logging.INFO)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            logging.info("Conectando...")
            self.room_group_name = 'chat_room'
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            print("Conexão aceita.")
        except Exception as e:
            logging.error(f"Erro na conexão: {e}")

    async def disconnect(self, close_code):
        logging.info("Desconectando... Código: {close_code}")
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            logging.info(f"Mensagem recebida: {text_data}")  
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            username = text_data_json['username']
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username
                }
            )
        except json.JSONDecodeError as e:
            logging.error(f"Erro ao decodificar JSON: {e}")
        except KeyError as e:
            logging.error(f"Erro de chave faltando: {e}")
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")


    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))


class MyAsyncHttpConsumer(AsyncHttpConsumer):
    async def handle(self, body):
        path = self.scope['path']
        print(f"Recebendo requisição para: {path}")  # Log da requisição

        if path == '/':
            response_content = """
            <html>
                <head>
                    <title>ASGI</title>
                </head>
                <body>
                    <h1>Server ASGI is running!</h1>
                </body>
            </html>
            """
            response_status = 200
        elif path == '/test/':
            response_content = """
            <html>
                <head>
                    <title>ASGI test page</title>
                </head>
                <body>
                    <h1>Server ASGI is running!</h1>
                </body>
            </html>
            """
            response_status = 200
        else:
            response_content = """
            <html>
                <head>
                    <title>404 Not Found</title>
                </head>
                <body>
                    <h1>Error 404: Not Found</h1>
                </body>
            </html>
            """
            response_status = 404

        await self.send_response(
            response_status,
            response_content.encode('utf-8'),  # Converte a string HTML para bytes
            headers=[(b'Content-Type', b'text/html')]  # Define o tipo de conteúdo como HTML
        )
