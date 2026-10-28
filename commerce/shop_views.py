"""Customer pages that reuse the commerce service layer."""

from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from commerce.models import CartItem, Order, Product
from commerce.services.cart_service import (
    add_to_cart, get_cart, get_cart_subtotal_paise,
    remove_cart_item, set_cart_item_quantity,
)
from commerce.services.order_service import cancel_order, checkout, list_customer_orders


def _customer(request):
    return request.user.is_authenticated and not request.user.is_staff


def _error(exc):
    if hasattr(exc, "messages"):
        return " ".join(exc.messages)
    return str(exc)


@require_GET
def catalogue(request):
    return render(request, "shop/catalogue.html", {
        "products": Product.objects.filter(is_active=True).order_by("name"),
        "customer": _customer(request),
    })


def customer_login(request):
    if request.method == "POST":
        from django.contrib.auth import get_user_model
        user_model = get_user_model()
        username = user_model.objects.filter(email__iexact=request.POST.get("email", "")).values_list("username", flat=True).first()
        user = authenticate(request, username=username, password=request.POST.get("password", "")) if username else None
        if user and user.is_active and not user.is_staff:
            login(request, user)
            return redirect("shop-catalogue")
        return render(request, "shop/login.html", {"error": "Invalid customer credentials"}, status=400)
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET", "POST"])
    return render(request, "shop/login.html")


@require_POST
def customer_logout(request):
    logout(request)
    return redirect("shop-catalogue")


def _cart_page(request, error=None):
    return render(request, "shop/cart.html", {
        "items": get_cart(request.user),
        "subtotal_paise": get_cart_subtotal_paise(request.user),
        "error": error,
    })


@require_GET
def cart(request):
    if not _customer(request):
        return redirect("shop-login")
    return _cart_page(request)


@require_POST
def cart_add(request):
    if not _customer(request):
        return redirect("shop-login")
    try:
        add_to_cart(request.user, int(request.POST["product_id"]), int(request.POST["quantity"]))
    except (ValidationError, ValueError, KeyError, Product.DoesNotExist, CartItem.DoesNotExist) as exc:
        return render(request, "shop/catalogue.html", {
            "products": Product.objects.filter(is_active=True).order_by("name"),
            "customer": True, "error": _error(exc),
        }, status=400)
    return redirect("shop-cart")


@require_POST
def cart_update(request, item_id):
    if not _customer(request):
        return redirect("shop-login")
    try:
        quantity = int(request.POST["quantity"])
        if quantity == 0:
            remove_cart_item(request.user, item_id)
        else:
            set_cart_item_quantity(request.user, item_id, quantity)
    except (ValidationError, ValueError, KeyError, Product.DoesNotExist, CartItem.DoesNotExist) as exc:
        return _cart_page(request, _error(exc))
    return redirect("shop-cart")


@require_POST
def place_order(request):
    if not _customer(request):
        return redirect("shop-login")
    try:
        checkout(
            request.user,
            coupon_code=request.POST.get("coupon_code", ""),
            shipping_name=request.POST.get("shipping_name", "").strip(),
            shipping_phone=request.POST.get("shipping_phone", "").strip(),
            shipping_address=request.POST.get("shipping_address", "").strip(),
        )
    except ValidationError as exc:
        return _cart_page(request, _error(exc))
    return redirect("shop-orders")


@require_GET
def orders(request):
    if not _customer(request):
        return redirect("shop-login")
    return render(request, "shop/orders.html", {"orders": list_customer_orders(request.user)})


@require_POST
def cancel(request, order_id):
    if not _customer(request):
        return redirect("shop-login")
    try:
        cancel_order(order_id, actor=request.user, customer=request.user,
                     reason=request.POST.get("reason", "Customer request"))
    except (ValidationError, Order.DoesNotExist) as exc:
        return render(request, "shop/orders.html", {
            "orders": list_customer_orders(request.user), "error": _error(exc),
        }, status=400)
    return redirect("shop-orders")
