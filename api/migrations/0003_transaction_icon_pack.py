# Generated by Django 4.2.10 on 2024-03-22 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_appuser_location_alter_preference_male_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='icon_pack',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.iconpack'),
        ),
    ]
