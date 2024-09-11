from django.contrib import admin
from unfold.admin import ModelAdmin
from django.contrib.auth.models import User, Group
from .models import Menyu, Food, Xabarlar, Users, Savat, Buyurtmalar, Karta
from django.utils.html import format_html

# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Menyu)
class AdminMenyu(ModelAdmin):
    list_display = ('name', 'photo')


@admin.register(Food)
class AdminFood(ModelAdmin):
    list_display = ('name', 'menyu', 'big_price', 'small_price')


@admin.register(Xabarlar)
class AdminXabar(ModelAdmin):
    list_display = ('text', 'author', 'author_id','username')
  

@admin.register(Users)
class AdminUser(ModelAdmin):
    list_display = ('user_id', 'fullname', 'username', 'phone')


@admin.register(Savat)
class AdminSavat(ModelAdmin):
    list_display = ('user', 'user_id', 'name', 'count', 'price', 'total_price')


@admin.register(Buyurtmalar)
class AdminBuyurtmalar(ModelAdmin):
    list_display = ('user', 'user_id', 'name', 'count', 'price', 'total_price', 'created', 'pay', 'status_colored')

    def status_colored(self, obj):
        if obj.status == 'qabul qilingan ✅':
            return format_html('<span style="color: green;">{}</span>', obj.status)
        elif obj.status == 'bekor qilingan ❌':
            return format_html('<span style="color: red;">{}</span>', obj.status)
        else:
            return obj.status

    status_colored.short_description = 'Buyurtma holati'


@admin.register(Karta)
class AdminKarta(ModelAdmin):
    list_display = ('qr_code_photo', 'card_number', 'card_user')

    def has_add_permission(self, request):
        if Karta.objects.count() >= 1:
            return False
        else:
            return True
    
