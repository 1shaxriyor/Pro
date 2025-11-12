from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
import requests

BOT_TOKEN = "8324626703:AAFrald_VmXTDhs6osCOvVmP-wZR7rQr0Gs"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@receiver(post_save, sender=Order)
def notify_master_on_new_order(sender, instance, created, **kwargs):
    if created and instance.master and instance.master.telegram_id:
        text = (
            f"🆕 Yangi buyurtma!\n"
            f"Xizmat: {instance.service_name}\n"
            f"Tavsif: {instance.description}\n\n"
            f"/accept_{instance.id}  ✅ Qabul qilish\n"
            f"/reject_{instance.id}  ❌ Rad etish"
        )
        requests.post(f"{BASE_URL}/sendMessage", json={
            "chat_id": instance.master.telegram_id,
            "text": text
        })
