from django.contrib import admin
from vapp.models import Product, Review, Wishlist, ContactMessage

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','cat','brand','stock','is_active']
    list_filter=['cat','is_active','brand']
    search_fields=['name','brand','pdetails']

class ReviewAdmin(admin.ModelAdmin):
    list_display=['product','user','rating','created_at']
    list_filter=['rating','created_at']
    search_fields=['product__name','user__username','comment']

class WishlistAdmin(admin.ModelAdmin):
    list_display=['user','product','added_at']
    list_filter=['added_at']
    search_fields=['user__username','product__name']

class ContactMessageAdmin(admin.ModelAdmin):
    list_display=['name','email','mobile','created_at','is_read']
    list_filter=['is_read','created_at']
    search_fields=['name','email','message']
    
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)    