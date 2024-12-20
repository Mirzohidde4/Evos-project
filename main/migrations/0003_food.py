# Generated by Django 5.1 on 2024-08-21 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_menyu_des_menyu_photo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('big_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('small_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('menyu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.menyu')),
            ],
        ),
    ]
