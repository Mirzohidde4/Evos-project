# Generated by Django 5.0.4 on 2024-08-30 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_alter_buyurtmalar_count_alter_buyurtmalar_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='xabarlar',
            name='username',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='foydalanuvchi nomi'),
        ),
    ]
