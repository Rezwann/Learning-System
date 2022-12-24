from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Subject, SubjectCategory
from .serializers import SubjectSerializer, SubjectCategorySerializer

@api_view(['GET'])
def get_subjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_subject_categories(request):
    subject_categories = SubjectCategory.objects.all()
    serializer = SubjectCategorySerializer(subject_categories, many=True)
    return Response(serializer.data)

