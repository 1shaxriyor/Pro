from django.db import models
from django.utils.text import slugify
from django.urls import reverse

def unique_slugify(instance, value, slug_field_name='slug', queryset=None, separator='-'):
    slug_base = slugify(value)
    slug = slug_base
    ModelsClass = instance.__class__
   if queryset is None:
        queryset = ModelClass._default_manager.all()
    if instance.pk:                        
        queryset = queryset.exclude(pk=instance.pk)
    i = 1
    while queryset.filter(**{slug_field_name: slug}).exists():  
        slug = f"{slug_base}{separator}{i}" 
        i += 1
    return slug

class Service(models.Models):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(null=True, blank=True,)  
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0,)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

  class Meta:
        verbose_name = "Xizmat"             
        verbose_name_plural = "Xizmatlar"
        ordering = ['name']                 

    def __str__(self):
        return self.name                    

    def save(self, *args, **kwargs):
        if not self.slug and self.name:     # agar slug hali yo‘q bo‘lsa
            self.slug = _unique_slugify(self, self.name)  # name dan avtomatik yaratish
        super().save(*args, **kwargs)       # asosiy saqlash funksiyasini chaqirish

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'slug': self.slug})  