# Generated by Django 4.1.7 on 2023-03-28 05:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('restaurant', '0002_alter_restaurant_adress_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='perm',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Группы прав'),
            preserve_default=False,
        ),
    ]
