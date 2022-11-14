from django.contrib import admin
from .models import Room, Amenity

@admin.action(description="Set all prices to zero")
def reset_prices(model_admin, request, queryset):
    # print(request.user) # 호출한 유저
    for room in queryset.all():
        room.price = 0
        room.save()


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    
    actions = (reset_prices,)
    
    list_display = (
        "name",
        "price",
        "kind",
        "total_amenities",
        "average_rating",
        "address",
        "owner"
    )
    
    def total_amenities(self, room): # self = 패널 자체
        return room.amenities.count()
    
    list_filter = (
        "country", 
        "city",
        "price",
        "pets_allowed",
        "kind",
        "category",
    )
    search_fields = (
        "owner__username",
    )

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    
    list_display = (
        "name",
        "created_at",
        "updated_at"
    )
    
    list_filter = (
        "created_at",
        "updated_at",
    )
    
    readonly_fields = (
        "created_at",
        "updated_at"
    )