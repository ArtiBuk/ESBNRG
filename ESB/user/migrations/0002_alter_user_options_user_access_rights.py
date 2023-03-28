# Generated by Django 4.1.7 on 2023-03-28 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AddField(
            model_name='user',
            name='access_rights',
            field=models.CharField(choices=[('Административно управленческий персонал', 'Административно управленческий персонал'), ('Операционный директор фастфудов', 'Операционный директор фастфудов'), ('Операционный директор ресторанов', 'Операционный директор ресторанов'), ('Операционный директор детских центров', 'Операционный директор детских центров'), ('Менеджер ПапаДжонс Талнах', 'Менеджер ПапаДЖонс Талнах')], default=1, max_length=256, verbose_name='Права доступа'),
            preserve_default=False,
        ),
    ]
