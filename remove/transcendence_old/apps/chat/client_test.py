import asyncio
import websockets
import json

async def chat_client():
    async with websockets.connect('ws://localhost:8001/ws/chat/') as websocket:
        # Enviar uma mensagem
        message = input("Digite sua mensagem: ")
        await websocket.send(json.dumps({'message': message}))
        
        # Receber a resposta
        response = await websocket.recv()
        data = json.loads(response)
        print(f"Resposta do servidor: {data['message']}")

if __name__ == '__main__':
    asyncio.run(chat_client())
