# Generated by Django 4.1.7 on 2023-04-25 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_user_access_rights'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='access_rights',
            field=models.ForeignKey(blank=True, default=25, on_delete=django.db.models.deletion.PROTECT, to='user.rightuser', verbose_name='Права доступа пользователя'),
        ),
    ]