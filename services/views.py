from django.shortcuts import render, get_object_or_404
from .models import Service, Master

def services_list(request):
    services = Service.objects.all()
    return render(request, "service/service_list.html", {"services": services})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    masters = Master.objects.filter(service=service)
    return render(request, "service/service_detail.html", {"service": service, "masters": masters})
