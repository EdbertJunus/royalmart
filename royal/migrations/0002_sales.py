# Generated by Django 4.2.6 on 2023-10-13 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('royal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sales_name', models.CharField(max_length=255, verbose_name='sales_name')),
                ('sales_file', models.FileField(upload_to='')),
            ],
        ),
    ]
