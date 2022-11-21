from rest_framework.test import APITestCase
from . import models

class TestAmenities(APITestCase):
    
    NAME = "Amenity Test"
    DESC = "Amenity desc"
    
    URL = "/api/v1/rooms/amenities"
    
    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC
        )
    
    def test_all_amenities(self):
        
        """ 모든 amenity list를 반환하는 public url인지 테스트 """
        
        response = self.client.get(self.URL) # 해당 url로 get 요청 보내기
        data = response.json() # 실제 데이터베이스 상에서 테스트하는 것이 아니라서 실제 데이터를 받아올 수는 없음
        self.assertEqual(response.status_code, 200, "Status code isn't 200.") # public url인가 (로그인 안해도 접근 가능)
        self.assertIsInstance(data, list) # 받아온 데이터 타입이 리스트 클래스에 속하는 가
        self.assertEqual(len(data), 1, "length is not 1")
        self.assertEqual(data[0]["name"], self.NAME, "name error")
        self.assertEqual(data[0]["description"], self.DESC, "desc error")
        
        
    def test_create_amenity(self):
        
        """ validated data와 exception 테스트 """
        
        new_amenity_name = "new Amenity"
        new_amenity_desc = "new one"
        
        # valid data
        response = self.client.post(
            self.URL, 
            data={"name":new_amenity_name, "description":new_amenity_desc}
        )
        data = response.json() # 생성한 데이터
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], new_amenity_name, "name not equal")
        self.assertEqual(data["description"], new_amenity_desc, "desc not equal")
        
        
        # invalid data
        response = self.client.post(self.URL)
        data = response.json() # 생성한 데이터
        self.assertEqual(response.status_code, 400)
        self.assertIn("names", data)
        