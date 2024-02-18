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
        # Call the parent class save method
        super().save(*args, **kwargs)

        # Sort and move icon pack images to their respective folder
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


class Preference(models.Model):
    image = models.ImageField(upload_to=generate_filename)
    color = models.CharField(max_length=6)
    male = models.BooleanField()

    style_1_Code = models.CharField(max_length=100)
    style_1_Image = models.ImageField(
        upload_to=generate_preferance_image_filename, null=True, blank=True)

    style_2_Code = models.CharField(max_length=100)
    style_2_Image = models.ImageField(
        upload_to=generate_preferance_image_filename, null=True, blank=True)

    icon_pack = models.ForeignKey(
        IconPack, on_delete=models.CASCADE, null=True, blank=True)


class AppUser(models.Model):
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
