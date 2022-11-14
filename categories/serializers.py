from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    
    # serializer 설정
    class Meta():
        model = Category # Category 모델을 위한 serializer를 만들어라
        
        # 무슨 field를 보일 지 선택
        fields = ("name", "kind") #1. 보여줄 field 선택
        #exclude = ("created_at") #2. 제외할 field 선택
        #fields = "__all__" # model의 모든 field 보여주겠다