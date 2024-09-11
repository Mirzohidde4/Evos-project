# Generated by Django 5.0.4 on 2024-08-30 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_alter_buyurtmalar_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyurtmalar',
            name='count',
            field=models.IntegerField(verbose_name='mahsulot soni'),
        ),
        migrations.AlterField(
            model_name='buyurtmalar',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='buyurtma berilgan sana'),
        ),
        migrations.AlterField(
            model_name='buyurtmalar',
            name='name',
            field=models.TextField(verbose_name='mahsulot nomi'),
        ),
        migrations.AlterField(
            model_name='buyurtmalar',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='mahsulot narxi'),
        ),
        migrations.AlterField(
            model_name='buyurtmalar',
            name='user_id',
            field=models.BigIntegerField(verbose_name='id raqami'),
        ),
        migrations.AlterField(
            model_name='karta',
            name='card_number',
            field=models.DecimalField(decimal_places=0, max_digits=16, verbose_name='karta raqami'),
        ),
        migrations.AlterField(
            model_name='karta',
            name='card_user',
            field=models.CharField(max_length=150, verbose_name='karta egasi'),
        ),
        migrations.AlterField(
            model_name='karta',
            name='qr_code_photo',
            field=models.ImageField(upload_to='media/karta', verbose_name='qr code'),
        ),
        migrations.AlterField(
            model_name='savat',
            name='count',
            field=models.IntegerField(verbose_name='mahsulot soni'),
        ),
        migrations.AlterField(
            model_name='savat',
            name='name',
            field=models.TextField(verbose_name='mahsulot nomi'),
        ),
        migrations.AlterField(
            model_name='savat',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='mahsulot narxi'),
        ),
        migrations.AlterField(
            model_name='savat',
            name='user_id',
            field=models.BigIntegerField(verbose_name='id raqami'),
        ),
        migrations.AlterField(
            model_name='users',
            name='fullname',
            field=models.CharField(max_length=150, verbose_name="to'liq ismi"),
        ),
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.CharField(max_length=13, verbose_name='telefon raqami'),
        ),
        migrations.AlterField(
            model_name='users',
            name='user_id',
            field=models.BigIntegerField(verbose_name='id raqami'),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='foydalanuvchi nomi'),
        ),
        migrations.AlterField(
            model_name='xabarlar',
            name='author_id',
            field=models.BigIntegerField(verbose_name='id raqami'),
        ),
        migrations.AlterField(
            model_name='xabarlar',
            name='username',
            field=models.CharField(max_length=150, verbose_name='foydalanuvchi nomi'),
        ),
    ]
