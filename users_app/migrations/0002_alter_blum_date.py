# Generated by Django 5.0.7 on 2024-07-29 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blum',
            name='date',
            field=models.DateField(),
        ),
    ]
