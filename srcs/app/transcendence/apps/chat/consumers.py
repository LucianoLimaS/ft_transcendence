import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()  # Aceita a conexão

    async def disconnect(self, close_code):
        # Aqui você pode lidar com a desconexão, se necessário
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)  # Decodifica a mensagem recebida
        message = data.get('message', '')

        # Envia uma resposta ao cliente
        await self.send(text_data=json.dumps({
            'message': f'Mensagem recebida: {message}'
        }))


# srcs/app/transcendence/apps/chat/consumers.py
from channels.generic.http import AsyncHttpConsumer

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
