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
        
        
        # invalid data - data missed
        response = self.client.post(self.URL)
        data = response.json() # 생성한 데이터
        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)
        
        # invalid data - validation error
        response = self.client.post(
            self.URL, 
            data={
                'name':"aaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbcccccccccccccccccccccdddddddddddddddddddddddddddddddddddddddddddeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeffffffffffffffffffffffffffffffffffgggggggggggggggggggggghhhhhhhhhhhiiiiiiiiiijjjjjjjjjkkkkkkkkkkkllllllmmmmmmmmmmmnoppppppppppp", 
                'description':self.DESC
            }
        )
        data = response.json() # 생성한 데이터
        
        self.assertEqual(response.status_code, 400)
                

class TestAmenity(APITestCase):
    
    NAME = "Amenity Test"
    DESC = "Amenity desc"
    
    URL = "/api/v1/rooms/amenities/"
    
    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC
        )
        
    def test_amenity_not_found(self):
        response = self.client.get(self.URL+"2")
        self.assertEqual(response.status_code, 404) # amenity가 없는 경우 에러 발생하는 지 테스트

    def test_get_amenity(self):
        response = self.client.get(self.URL+"1")
        self.assertEqual(response.status_code, 200) # amenity가 존재하는 경우 통과하는 지 확인
        
        data = response.json()
        
        self.assertEqual(data['name'], self.NAME)
        self.assertEqual(data['description'], self.DESC)
    
    def test_put_amenity(self):
        # valid data
        
        new_name = "PUT TEST name"
        new_desc = "PUT TEST desc"
        
        response = self.client.put(self.URL+"1", data={"name":new_name, "description":new_desc})
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        
        self.assertEqual(data['name'], new_name)
        self.assertEqual(data['description'], new_desc)
        
        # invalid data
        response = self.client.put(self.URL+"1", data={"name": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"})
        data = response.json()
        
        self.assertEqual(response.status_code, 400, "maxLength validation doesn't work!")
        
    
    def test_delete_amenity(self):
        response = self.client.delete(self.URL+"1")
        self.assertEqual(response.status_code, 204) # 삭제되는지 확인
        
        