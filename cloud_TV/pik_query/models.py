from django.db import models

# Create your models here.

class Images(models.Model):
    name=models.CharField(max_length=200, primary_key=True)
    image=models.ImageField(upload_to='image_orig/')

    def __str__(self):
        return self.name
