# Generated by Django 5.1 on 2024-08-29 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_buyurtmalar_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='foydalanuvchi_nomi'),
        ),
    ]