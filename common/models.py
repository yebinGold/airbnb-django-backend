from django.db import models


class CommonModel(models.Model):
    
    """Common Model Definition"""
    
    created_at = models.DateTimeField(auto_now_add=True) # object가 처음 생성된 시간
    updated_at = models.DateTimeField(auto_now=True) # object가 저장될 때마다 시간 업데이트
    
    
    class Meta: # 장고에서 model을 configure할 때 사용하는 클래스
        abstract = True # DB에 저장 안 함