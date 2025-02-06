from django.db import models
from django.forms import ValidationError

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
    
    class Meta:
        verbose_name_plural = "Hotels"
        ordering = ['name']
    
    def clean(self):
        self.code = self.code.strip().upper()
        self.name = self.name.strip()
        
        if len(self.code) != 5:
            raise ValidationError('The hotel code must be 3 characters long')
        
        if not self.name:
            raise ValidationError('The hotel name cannot be empty')
        
        if not self.city:
            raise ValidationError('The hotel must belong to a city')
        if not City.objects.filter(pk=self.city.pk).exists():
            raise ValidationError('The hotel must belong to an existing city')
        
        

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
        
    def clean(self):
        self.code = self.code.strip().upper()
        self.name = self.name.strip()
        
        if len(self.code) != 3:
            raise ValidationError('The city code must be 3 characters long')
        
        if not self.name:
            raise ValidationError('The city name cannot be empty')

    def __str__(self):
        return f"{self.name} ({self.code})"