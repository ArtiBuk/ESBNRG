# Generated by Django 4.1.7 on 2023-03-28 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_access_rights'),
        ('restaurant', '0005_restaurant_perm'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='perm',
            new_name='perm_grup_fo',
        ),
        migrations.AddField(
            model_name='restaurantcategory',
            name='perm_grup_for_category',
            field=models.ManyToManyField(to='user.rightuser', verbose_name='Группы прав'),
        ),
    ]
