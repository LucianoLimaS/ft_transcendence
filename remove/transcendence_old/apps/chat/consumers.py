from channels.generic.websocket import WebsocketConsumer
from channels.generic.http import AsyncHttpConsumer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

class MyAsyncHttpConsumer(AsyncHttpConsumer):
    async def handle(self):
        print("Test OK")