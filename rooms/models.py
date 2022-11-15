from django.db import models
from common.models import CommonModel

# Create your models here.

class Room(CommonModel):
    
    """Room Model Definition"""
    
    class RoomKindChoices(models.TextChoices):
        ENTIRE_PLACE = "entire_place", "Entire Place"
        PRIVATE_ROOM = "private_room", "Private Room"
        SHARED_ROOM = "shared_room", "Shared Room"
    
    name = models.CharField(max_length=150, default="")
    country = models.CharField(max_length=50, default="South Korea")
    city = models.CharField(max_length=80, default="Seoul")
    price = models.PositiveIntegerField()
    rooms = models.PositiveIntegerField()
    toilets = models.PositiveIntegerField()
    desc = models.TextField()
    address = models.CharField(max_length=250)
    pets_allowed = models.BooleanField(default=True)
    kind = models.CharField(max_length=20, choices=RoomKindChoices.choices)
    owner = models.ForeignKey("users.User",
                              on_delete=models.CASCADE,
                              related_name="rooms"
                              )
    amenities = models.ManyToManyField("rooms.Amenity", related_name="rooms")
    category = models.ForeignKey("categories.Category", 
                                 null=True, 
                                 blank=True, 
                                 on_delete=models.SET_NULL,
                                 related_name="rooms",
                                 )
    
    def __str__(self) -> str:
        return self.name
    
    def average_rating(self):
        count = self.reviews.count()
        if count == 0:
            return 0
        else:
            total_rating = 0
            for ratings in self.reviews.all().values("rating"):
                total_rating += ratings['rating']
            return round(total_rating / count, 1)
                

    
class Amenity(CommonModel):
        
    """Amenity Definition"""
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=150, null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Amenities"