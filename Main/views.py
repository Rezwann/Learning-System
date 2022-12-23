from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Subject
from .serializers import SubjectSerializer

@api_view(['GET'])
def get_subjects(request):
    subjects = Subject.objects.all()
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)

