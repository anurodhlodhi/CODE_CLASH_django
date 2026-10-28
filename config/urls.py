
from django.contrib import admin
from django.urls import include, path

from commerce.admin_views import operations_dashboard
from commerce import shop_views


urlpatterns = [
    path("", shop_views.catalogue, name="shop-catalogue"),
    path("shop/", shop_views.catalogue, name="shop-home"),
    path("shop/login/", shop_views.customer_login, name="shop-login"),
    path("shop/logout/", shop_views.customer_logout, name="shop-logout"),
    path("shop/cart/", shop_views.cart, name="shop-cart"),
    path("shop/cart/add/", shop_views.cart_add, name="shop-cart-add"),
    path("shop/cart/<int:item_id>/update/", shop_views.cart_update, name="shop-cart-update"),
    path("shop/checkout/", shop_views.place_order, name="shop-checkout"),
    path("shop/orders/", shop_views.orders, name="shop-orders"),
    path("shop/orders/<int:order_id>/cancel/", shop_views.cancel, name="shop-order-cancel"),
    # Keep this custom route before the main admin route.
    path(
        "admin/commerce/operations/",
        admin.site.admin_view(operations_dashboard),
        name="commerce-admin-operations",
    ),

    path("admin/", admin.site.urls),
    path("api/", include("commerce.urls")),
]
