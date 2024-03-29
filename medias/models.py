from django.db import models
from common.models import CommonModel

# Create your models here.
class Photo(CommonModel):
    
    file = models.URLField()
    description = models.CharField(max_length=140, null=True, blank=True,)
    room = models.ForeignKey("rooms.Room", null=True, blank=True, on_delete=models.CASCADE, related_name="photos")
    experience = models.ForeignKey("experiences.Experience", null=True, blank=True, on_delete=models.CASCADE, related_name="photos")
    
    def __str__(self) -> str:
        return "Photo file"


class Video(CommonModel):
    
    file = models.URLField()
    experience = models.OneToOneField("experiences.Experience", on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return "Video file"