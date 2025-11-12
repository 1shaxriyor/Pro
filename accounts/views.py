from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, ProfileForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib import messages
from django.conf import settings
from .models import TelegramConnectToken
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class HomeView(View):
    def get(self, request):
        return render(request, 'home.html')

class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan muvaffaqiyatli o'tdingiz.")
            return redirect('home')
        return render(request, 'accounts/register.html', {'form': form})

class LoginView(DjangoLoginView):
    template_name = 'accounts/login.html'

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil yangilandi.")
            return redirect('profile')
        return render(request, 'accounts/profile.html', {'form': form})

class IntegrationView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'accounts/integration.html', {
            'telegram_id': request.user.telegram_id,
            'TELEGRAM_BOT_USERNAME': settings.TELEGRAM_BOT_USERNAME
        })

@method_decorator(login_required, name='dispatch')
class TelegramLoginLinkView(View):
    """
    AJAX POST from frontend (Telegram Login Widget) with Telegram fields.
    Backend verifies hash per Telegram docs and saves telegram_id for request.user.
    """
    def post(self, request):
        data = {}
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode())
            except:
                data = {}
        else:
            data = request.POST.dict()

        tg_hash = data.get('hash')
        if not tg_hash:
            return JsonResponse({'detail': 'No hash provided'}, status=400)

        # verify hash
        import hashlib, hmac
        bot_token = settings.TELEGRAM_BOT_TOKEN
        secret_key = hashlib.sha256(bot_token.encode()).digest()

        data_check_arr = []
        for k, v in sorted((k, v) for k, v in data.items() if k != 'hash'):
            data_check_arr.append(f"{k}={v}")
        data_check_string = "\n".join(data_check_arr).encode()

        h = hmac.new(secret_key, data_check_string, hashlib.sha256).hexdigest()
        if h != tg_hash:
            return JsonResponse({'detail': 'Invalid data (hash mismatch)'}, status=403)

        telegram_id = data.get('id') or data.get('user_id')
        if telegram_id:
            user = request.user
            user.telegram_id = str(telegram_id)
            user.save(update_fields=['telegram_id'])
            return JsonResponse({'detail': 'Telegram connected', 'telegram_id': telegram_id})
        return JsonResponse({'detail': 'No telegram id'}, status=400)

# Token generator (bot linking) view
@login_required
def generate_bot_token_view(request):
    token_obj = TelegramConnectToken.objects.create(user=request.user)
    return JsonResponse({'token': str(token_obj.token)})