from django.contrib import admin
from .models import Review

class RateFilter(admin.SimpleListFilter):
    title = "Good reviews or Bad reviews"
    parameter_name = "rate" # url 파라미터로 쓸 이름
    
    def lookups(self, request, model_admin): # self, 호츌 요청 정보, 필터 사용할 어드민 클래스
        """필터링 키워드 보여주는 부분, 리스트를 반환"""
        return [
            ("good", "Good"), # (저장되는 값, 실제로 유저에게 보이는 값)
            ("bad", "Bad")
        ]
    
    def queryset(self, request, queryset): # 필터링 할 목록 받아옴
        # print(request.GET) # url을 읽어와서 선택한 키워드를 담은 딕셔너리를 줌
        word = self.value() # shortcut
        if word == 'good':
            return queryset.filter(rating__gte=3) # 필터링 결과 리턴
        elif word == "bad":
            return queryset.filter(rating__lt=3) # 필터링 결과 리턴
        
        return queryset

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "__str__", "payload",
    )

    list_filter = (RateFilter,
                   "rating",
                   "user__is_host",
                   "room__category",
                   )