# Generated by Django 4.2.10 on 2024-02-18 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='iconpack',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]