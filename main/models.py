from django.db import models

# Create your models here.
class Users(models.Model):
    user_id = models.BigIntegerField(verbose_name='id raqami')
    fullname = models.CharField(max_length=150, verbose_name='to\'liq ismi')
    username = models.CharField(max_length=150, verbose_name='foydalanuvchi nomi', null=True, blank=True)
    phone = models.CharField(max_length=13, verbose_name='telefon raqami')

    def __str__(self):
        return self.fullname

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class Menyu(models.Model):
    name = models.CharField(max_length=250)
    photo = models.ImageField(upload_to='media')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
  

class Food(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nomi')
    menyu = models.ForeignKey(to=Menyu, on_delete=models.CASCADE, verbose_name='Turi')
    descroption = models.TextField(blank=True, null=True)
    big_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Narxi')
    small_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Narxi(kichik)', blank=True, null=True)
    photo = models.ImageField(upload_to='media/food')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Taom'
        verbose_name_plural = 'Taomlar'


class Xabarlar(models.Model):
    text = models.TextField(verbose_name='xabar')
    author = models.CharField(max_length=100, verbose_name='foydalanuvchi')
    author_id = models.BigIntegerField(verbose_name='id raqami')
    username = models.CharField(max_length=150, verbose_name='foydalanuvchi nomi', blank=True, null=True)

    class Meta:
        verbose_name = 'Xabar'
        verbose_name_plural = 'Xabarlar'

    def __str__(self):
        return self.author  
  
  
class Savat(models.Model):
    user = models.CharField(max_length=100, verbose_name='foydalanuvchi')
    user_id = models.BigIntegerField(verbose_name='id raqami')
    name = models.TextField(verbose_name='mahsulot nomi')
    count = models.IntegerField(verbose_name='mahsulot soni')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='mahsulot narxi')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='umumiy narxi')
    
    class Meta:
        verbose_name = 'Savat'
        verbose_name_plural = 'Savatlar'

    def __str__(self):
        return self.user 


class Buyurtmalar(models.Model):
    user = models.CharField(max_length=100, verbose_name='foydalanuvchi')
    user_id = models.BigIntegerField(verbose_name='id raqami')
    name = models.TextField(verbose_name='mahsulot nomi')
    count = models.IntegerField(verbose_name='mahsulot soni')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='mahsulot narxi')
    total_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='umumiy narxi')
    created = models.DateTimeField(auto_now_add=True, verbose_name='buyurtma berilgan sana')
    pay = models.CharField(max_length=5, verbose_name='to\'lov turi')
    status = models.CharField(max_length=10, verbose_name='buyurtma holati')
    
    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'

    def __str__(self):
        return self.user 


class Karta(models.Model):
    qr_code_photo = models.ImageField(upload_to='media/karta', verbose_name='qr code')
    card_number = models.DecimalField(max_digits=16, decimal_places=0, verbose_name='karta raqami')
    card_user = models.CharField(max_length=150, verbose_name='karta egasi')

    class Meta:
        verbose_name = 'Karta'
        verbose_name_plural = 'Kartalar'

    def __str__(self):
        return self.card_user
            