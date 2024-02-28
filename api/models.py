import os
from django.core.validators import FileExtensionValidator
from django.db import models
import uuid


def get_filename(filename):
    # Generate a unique filename using a UUID
    extension = filename.split('.')[-1]
    _filename = f"{uuid.uuid4()}.{extension}"
    return _filename


def generate_filename(instance, filename):
    return f"wallpapers/{get_filename(filename)}"


def generate_preference_filename(instance, filename):
    return f"preference/{get_filename(filename)}"


def generate_filenameIconPreview(instance, filename):
    return f"icon-packs/icons/{get_filename(filename)}"


def generate_iconpack_image_filename(instance, filename):
    return f"icon-packs/previews/{get_filename(filename)}"


def generate_preferance_image_filename(instance, filename):
    return f"preference/previews/{get_filename(filename)}"


class IconPack(models.Model):
    active = models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    preview = models.ImageField(upload_to=generate_filenameIconPreview)
    icon_pack = models.FileField(upload_to=generate_iconpack_image_filename,
                                 validators=[FileExtensionValidator(allowed_extensions=["zip"])])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        icon_pack_folder = os.path.join("media/icon-packs", self.name)
        os.makedirs(icon_pack_folder, exist_ok=True)

        for image in self.iconpackimage_set.all():
            old_path = image.image_url.path
            new_filename = get_filename(old_path)
            new_path = os.path.join(icon_pack_folder, new_filename)

            os.rename(old_path, new_path)
            image.image_url.name = f"icon-packs/{self.name}/{new_filename}"
            image.save()

    def __str__(self):
        return self.name


class IconPackImage(models.Model):
    icon_pack = models.ForeignKey(IconPack, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=generate_iconpack_image_filename)


class Wallpaper(models.Model):
    title = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to=generate_filename)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Style(models.Model):
    name = models.CharField(max_length=100)
    style_code = models.CharField(max_length=100, unique=True)
    image_url = models.ImageField(upload_to=generate_filename)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=100)
    color_code = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Preference(models.Model):
    image = models.ImageField(upload_to=generate_filename,)
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, null=True, blank=True)

    male = models.BooleanField(default=True)

    style_1 = models.ForeignKey(
        Style, on_delete=models.CASCADE, null=True, blank=True, related_name='preference_style_1')
    style_2 = models.ForeignKey(
        Style, on_delete=models.CASCADE, null=True, blank=True, related_name='preference_style_2')

    icon_pack = models.ForeignKey(
        IconPack, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return self.image.name


class AppUser(models.Model):
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=6)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Transaction(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    sku = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
