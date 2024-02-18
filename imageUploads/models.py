from django.db import models
import os


# Create your models here.
class Image(models.Model):
    caption = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.caption

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
                super(Image, self).delete(*args, **kwargs)
