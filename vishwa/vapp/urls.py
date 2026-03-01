from django.urls import path
from vapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('products',views.products),
    path('about',views.about),
    path('contact',views.contact),
    path('login',views.user_login),
    path('register',views.register),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sortprice),
    path('pricefilter',views.pricefilter),
    path('product_details/<pid>',views.product_details),
    path('placeorder',views.placeorder),
    path('addcart/<pid>',views.cart),
    path('viewcart',views.viewcart), 
    path('updateqty/<x>/<cid>',views.updateqty),
    path('removecart/<cid>',views.removecart),
    path('fetchorder',views.fetchorderdetails),
    path('makepayment',views.makepayment),
    path('paymentsuccess',views.paymentsuccess),
    path('removeord/<oid>',views.removeord),
    path('profile',views.profile),
    path('shipping',views.shipping),
    path('privacy',views.privacy),
    path('terms',views.terms),
    path('orders', views.orders),
    path('api/cart-count/', views.cart_count, name='cart_count'),
    path('add_review/<pid>', views.add_review, name='add_review'),
    path('toggle_wishlist/<pid>', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist', views.wishlist, name='wishlist'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
