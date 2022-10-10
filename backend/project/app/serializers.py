from rest_framework import serializers
from . models import Subject, Question

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:

        model = Subject
        fields = ('id', 'name', 'image')

class QuestionEnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('en_lang', 'en_answer')

class QuestionRuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('ru_lang', 'ru_answer')
