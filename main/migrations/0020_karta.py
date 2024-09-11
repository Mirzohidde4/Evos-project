# Generated by Django 5.1 on 2024-08-29 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_alter_users_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Karta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qr_code_photo', models.ImageField(upload_to='media/karta', verbose_name='qr_code')),
                ('card_number', models.DecimalField(decimal_places=0, max_digits=16, verbose_name='karta_raqami')),
                ('card_user', models.CharField(max_length=150, verbose_name='karta_egasi')),
            ],
            options={
                'verbose_name': 'Karta',
                'verbose_name_plural': 'Kartalar',
            },
        ),
    ]
