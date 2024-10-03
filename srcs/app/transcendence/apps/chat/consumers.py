# srcs/app/transcendence/apps/chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()  # Aceita a conexão

    async def disconnect(self, close_code):
        pass  # Lógica de desconexão, se necessário

    async def receive(self, text_data):
        data = json.loads(text_data)
        # Processar dados recebidos
        await self.send(text_data=json.dumps({
            'message': 'Mensagem recebida com sucesso!'
        }))

# ft_transcendence/conversations.py
from channels.generic.http import AsyncHttpConsumer

class SimpleHtmlConsumer(AsyncHttpConsumer):
    async def handle(self, body):
        html_content = """
        <html>
            <head>
                <title>Test Page</title>
            </head>
            <body>
                <h1>Hello, ASGI!</h1>
                <p>This is a simple HTML page served by ASGI.</p>
            </body>
        </html>
        """
        await self.send_response(200, html_content.encode("utf-8"), headers=[
            (b"Content-Type", b"text/html"),
        ])
