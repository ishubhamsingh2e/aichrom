# Generated by Django 4.2.10 on 2024-02-12 08:55

import api.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('otp', models.CharField(max_length=6)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='IconPack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('preview', models.ImageField(upload_to=api.models.generate_filenameIconPreview)),
                ('icon_pack', models.FileField(upload_to=api.models.generate_iconpack_image_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['zip'])])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wallpaper',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image_url', models.ImageField(upload_to=api.models.generate_filename)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=api.models.generate_filename)),
                ('color', models.CharField(max_length=6)),
                ('male', models.BooleanField()),
                ('style_1_Code', models.CharField(max_length=100)),
                ('style_1_Image', models.ImageField(blank=True, null=True, upload_to=api.models.generate_preferance_image_filename)),
                ('style_2_Code', models.CharField(max_length=100)),
                ('style_2_Image', models.ImageField(blank=True, null=True, upload_to=api.models.generate_preferance_image_filename)),
                ('icon_pack', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.iconpack')),
            ],
        ),
        migrations.CreateModel(
            name='IconPackImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.ImageField(upload_to=api.models.generate_iconpack_image_filename)),
                ('icon_pack', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.iconpack')),
            ],
        ),
    ]
