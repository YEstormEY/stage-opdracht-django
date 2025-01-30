from django.db import models

# Create your models here.


class Hotel(models.Model):
    
    city = models.ForeignKey(
        'City',
        on_delete=models.CASCADE,
        related_name='hotels',
    )

    code = models.CharField(
        max_length=5,
        unique=True,
    )
    
    name = models.CharField(
        max_length=50,
    )

class City(models.Model):
    
    code = models.CharField(
        max_length=3,
        unique=True,
    )
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    
    class Meta:
        verbose_name_plural = "Cities"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"