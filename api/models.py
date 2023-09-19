from django.db import models
import uuid


def generate_filename(instance, filename):
    # Generate a unique filename using a UUID
    extension = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    return f"wallpapers/{filename}"


def generate_iconpackname(instance, filename):
    # Generate a unique filename using a UUID
    extension = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    return f"icon-packs/{filename}"


class IconPack(models.Model):
    name = models.CharField(max_length=100)
    icon_pack = models.FileField(upload_to=generate_iconpackname)
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
