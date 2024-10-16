from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.decorators import login_required
from django.views import View

@login_required
def chat_index(request):
    return render(request, 'chat/index.html')

def chat_test(request):
    return render(request, 'chat/test.html')

class ChatView(View):
    def get(self, request):
        # Lógica para renderizar a página de chat
        return render(request, 'chat/index.html')

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'chat_room',
            {
                'type': 'chat_message',
                'message': message
            }
        )
        return JsonResponse({'status': 'success', 'message': message})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)