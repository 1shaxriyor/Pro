from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from .models import User, TelegramConnectToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import JsonResponse
import json

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

class UserMeAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

@method_decorator(csrf_exempt, name='dispatch')
class BotWebhookView(View):
    """
    Bot tomonidan (yoki bot o'zi backendga) yuborilgan token+telegram_id ni qabul qiladi.
    JSON: {"token": "<uuid>", "telegram_id": 123456789}
    """
    def post(self, request):
        try:
            payload = json.loads(request.body.decode())
            token = payload.get('token')
            telegram_id = payload.get('telegram_id')
            if not token or not telegram_id:
                return JsonResponse({'detail': 'token or telegram_id missing'}, status=400)
            try:
                t = TelegramConnectToken.objects.get(token=token, used=False)
            except TelegramConnectToken.DoesNotExist:
                return JsonResponse({'detail': 'invalid token'}, status=400)
            user = t.user
            user.telegram_id = str(telegram_id)
            user.save(update_fields=['telegram_id'])
            t.used = True
            t.save(update_fields=['used'])
            return JsonResponse({'detail': 'ok'})
        except Exception as e:
            return JsonResponse({'detail': str(e)}, status=500)