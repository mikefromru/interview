from rest_framework import serializers
from . models import Subject, Question

class SubjectSerializer(serializers.ModelSerializer):

    class Meta:

        model = Subject
        fields = ('id', 'name', 'image')

class QuestionEnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'en_lang',)

class QuestionRuSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'ru_lang',)

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'
