# Generated by Django 4.1.7 on 2023-04-27 07:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0017_alter_report_weekdays'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='report',
            unique_together={('department', 'data')},
        ),
    ]
