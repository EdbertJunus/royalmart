# Generated by Django 4.2.6 on 2023-10-24 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('royal', '0002_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='supplier',
            field=models.CharField(default='', max_length=255),
        ),
    ]
