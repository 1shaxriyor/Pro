from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
import requests

BOT_TOKEN = "8324626703:AAFrald_VmXTDhs6osCOvVmP-wZR7rQr0Gs"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

@receiver(post_save, sender=Order)
def notify_master_or_client(sender, instance, created, **kwargs):
    """
    - Yangi order → masterga xabar
    - Status update (accepted/rejected) → clientga xabar
    """
    if created:
        # Yangi order → masterga
        if instance.master and instance.master.telegram_id:
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
    else:
        # Status update → clientga
        if instance.status in ["accepted", "rejected"]:
            text = f"📣 Sizning buyurtmangiz {instance.status} bo‘ldi!\nXizmat: {instance.service_name}"
            if instance.client.telegram_id:
                requests.post(f"{BASE_URL}/sendMessage", json={
                    "chat_id": instance.client.telegram_id,
                    "text": text
                })
