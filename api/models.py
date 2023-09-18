from django.db import models
import uuid


def generate_filename(instance, filename):
    # Generate a unique filename using a UUID
    extension = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    return f"wallpapers/{filename}"


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
