from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin): # 일반 모델 패널이 아닌 관리자 패널을 상속받음
    
    fieldsets = (
        ("Profile", {
            "fields": (
                "profile_photo", 
                "username", 
                "name", 
                "is_host", 
                "gender", 
                "language",
                "currency",
                ),
            },
        ),
        ("Permissions", {"fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",)
            },
        ),
        ("Important Dates", {"fields": ("last_login", "date_joined"),},),
    )
    
    list_display = ("username", "email", "name", "is_host")