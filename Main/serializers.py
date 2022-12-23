from rest_framework import serializers

from .models import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'details', 'category', 'year_group', 'subject_leader')