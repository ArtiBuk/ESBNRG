# Generated by Django 4.1.7 on 2023-03-23 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='adress',
            field=models.CharField(max_length=128, verbose_name='Адресc'),
        ),
        migrations.AlterUniqueTogether(
            name='restaurant',
            unique_together={('name', 'adress')},
        ),
    ]
