from django.db import models
from common.models import CommonModel

# Create your models here.
class Experience(CommonModel):
    
    """Experience Model Description"""
    
    name = models.CharField(max_length=250, default="")
    country = models.CharField(max_length=50, default="South Korea")
    city = models.CharField(max_length=80, default="Seoul")
    price = models.PositiveIntegerField()
    host = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="experiences")
    address = models.CharField(max_length=250)
    start = models.TimeField()
    end = models.TimeField()
    description = models.TextField()
    perks = models.ManyToManyField("experiences.Perk", related_name="experiences")
    category = models.ForeignKey("categories.Category", null=True, blank=True, on_delete=models.SET_NULL, related_name="experiences")
    
    def __str__(self) -> str:
        return self.name
    
    def average_rating(self):
        count = self.reviews.count()
        if count == 0:
            return 0
        total = 0
        for ratings in self.reviews.all().values('rating'):
            total += ratings["rating"]
        return round(total / count, 1)
    

class Perk(CommonModel):
    
    """ What is included on an Experience """
    
    name = models.CharField(max_length=150)
    detail = models.CharField(max_length=250, blank=True, default="")
    explanation = models.TextField(blank=True, default="")
    
    def __str__(self) -> str:
        return self.name