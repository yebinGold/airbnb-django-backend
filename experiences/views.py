from django.db import transaction

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from . import serializers
from .models import Perk, Experience
from categories.models import Category
from medias.serializers import PhotoSerializer


class Perks(APIView):
    
    def get(self, request):
        all_perks = Perk.objects.all()
        serlalizer = serializers.PerkSerializer(all_perks, many=True)
        return Response(serlalizer.data)
        
    def post(self, request):
        serializer = serializers.PerkSerializer(data=request.data)
        if serializer.is_valid():
            new_perk = serializer.save()
            return Response(serializers.PerkSerializer(new_perk).data)
        else:
            return Response(serializer.errors)


class PerkDetail(APIView):
    
    def get_object(self, pk):
        try:
            perk = Perk.objects.get(pk=pk)
            return perk
        except Perk.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk)
        return Response(serializer.data)
        
    def put(self, request, pk):
        perk = self.get_object(pk)
        serializer = serializers.PerkSerializer(perk, data=request.data, partial=True)
        if serializer.is_valid():
            updated_perk = serializer.save()
            return Response(serializers.PerkSerializer(updated_perk).data)
        else:
            return Response(serializer.errors)
        
    def delete(self, request, pk):
        perk = self.get_object(pk)
        perk.delete()
        return Response(status=status.HTTP_200_OK)
    
    
class Experiences(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        all_experiences = Experience.objects.all()
        serializer = serializers.ExperienceListSerializer(all_experiences, many=True)
        return Response(serializer.data)
    
    def post(self, request):
 
        serializer = serializers.ExperienceDetailSerializer(data=request.data)
        if serializer.is_valid():
            category_pk = request.data.get("category")
            if not category_pk:
                raise ParseError("Category is required.")
            try:
                category = Category.objects.get(pk=category_pk)
                if category.kind == Category.CategoryKindChoices.ROOMS:
                    raise ParseError("The category kind should be 'experiences'")
            except Category.DoesNotExist:
                raise ParseError("Category not found")
            try:
                with transaction.atomic():
                    new_experience = serializer.save(host=request.user, category=category)
                    perks = request.data.get("perks") # 추가할 perk id 리스트
                    for perk_pk in perks:
                        perk = Perk.objects.get(pk=perk_pk)
                        new_experience.perks.add(perk)
                    return Response(serializers.ExperienceDetailSerializer(new_experience).data)
            except Exception:
                raise ParseError("Perk not found")
        else:
            return Response(serializer.errors)
        
        
class ExperienceDetail(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound
    
    def get(self, request, pk):
        experience = self.get_object(pk)
        serializer = serializers.ExperienceDetailSerializer(experience)
        return Response(serializer.data)
    
    def put(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        serializer = serializers.ExperienceDetailSerializer(experience, data=request.data, partial=True, context={"pk":pk})
        
        if request.data.get("category"):
            try:
                category_pk = request.data.get("category")
                new_category = Category.objects.get(pk=category_pk)
                if new_category.kind != Category.CategoryKindChoices.EXPERIENCES:
                    category = experience.category
                    raise ParseError("Category kind should be 'experience'")
                else: 
                    category = new_category
            except Category.DoesNotExist:
                raise ParseError("Category not found")
        else:
            category = experience.category
            
        if serializer.is_valid():
            try:
                with transaction.atomic(): 
                    updated_experience = serializer.save(category=category)
                    
                    if request.data.get("perks"):
                        new_perks = request.data.get("perks")
                        updated_experience.perks.clear()
                        for perk_pk in new_perks:
                            perk = Perk.objects.get(pk=perk_pk)
                            updated_experience.perks.add(perk)
                    return Response(serializers.ExperienceDetailSerializer(updated_experience).data)
            except Exception:
                raise ParseError("Perk not found")
        else:
            return Response(serializer.errors)
            
    def delete(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        experience.delete()
        return Response(status=status.HTTP_200_OK)
    
    
class ExperiencePerks(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound
     
    def get(self, request, pk):
        experience = self.get_object(pk)
        all_perks = experience.perks.all()
        serializer = serializers.PerkSerializer(all_perks, many=True)
        return Response(serializer.data)


class ExperiencePhotos(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Experience.objects.get(pk=pk)
        except Experience.DoesNotExist:
            raise NotFound
        
    def post(self, request, pk):
        experience = self.get_object(pk)
        if experience.host != request.user:
            raise PermissionDenied
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(experience=experience)
            return Response(PhotoSerializer(photo).data)
        else: 
            return Response(serializer.errors)
        
    
    