# Generated by Django 4.1.7 on 2023-03-28 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_remove_user_is_verified_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='access_rights',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='user.rightuser', verbose_name='Права доступа пользователя'),
        ),
    ]