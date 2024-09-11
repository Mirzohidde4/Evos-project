# Generated by Django 4.2 on 2024-08-21 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_food_options_alter_menyu_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menyu',
            name='des',
        ),
        migrations.AddField(
            model_name='food',
            name='photo',
            field=models.ImageField(default=2, upload_to='media/food'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='food',
            name='small_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Narxi'),
        ),
    ]