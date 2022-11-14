from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    
    class GenderChoices(models.TextChoices):
        # OPTION = ("value", "label on the admin panel")
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")
    class LanguageChoices(models.TextChoices):
        KR = ("kr", "Korean")
        EN = ("en", "English")
    class CurrencyChoices(models.TextChoices):
        WON = "won", "Korean Won"
        USD = "usd", "US Dollar"
    
    # overriding
    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    
    # custom
    name = models.CharField(max_length=150, default="")
    is_host = models.BooleanField(default=False)
    profile_photo = models.ImageField(blank=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    language = models.CharField(max_length=2, choices=LanguageChoices.choices)
    currency = models.CharField(max_length=5, choices=CurrencyChoices.choices)