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


def generate_filenameIconPreview(instance, filename):
    return f"icon-packs/preview/{get_filename(filename)}"


def generate_iconpackname(instance, filename):
    return f"icon-packs/{get_filename(filename)}"


class IconPack(models.Model):
    name = models.CharField(max_length=100)
    preview = models.ImageField(upload_to=generate_filenameIconPreview)
    icon_pack = models.FileField(upload_to=generate_iconpackname,
                                 validators=[FileExtensionValidator(allowed_extensions=["zip"])])
    tags = models.ManyToManyField('Tag', related_name='icon_packs')

    def __str__(self):
        return self.name


class Wallpaper(models.Model):
    title = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to=generate_filename)
    tags = models.ManyToManyField('Tag', related_name='wallpapers')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
