from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_form_view(request):
    if request.method == "POST":
        service_name = request.POST.get("service_name")
        description = request.POST.get("description")
        Order.objects.create(client=request.user, service_name=service_name, description=description)
        return redirect("orders:orders_list")
    return render(request, "orders/order_form.html")

@login_required
def orders_list_view(request):
    orders = Order.objects.filter(client=request.user)
    return render(request, "orders/orders_list.html", {"orders": orders})

@login_required
def master_orders_view(request):
    orders = Order.objects.filter(master=request.user)
    return render(request, "orders/master_orders.html", {"orders": orders})
