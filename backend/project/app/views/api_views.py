from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from .. models import Subject, Question
from .. serializers import (
    SubjectSerializer,
    QuestionEnSerializer,
    QuestionRuSerializer,
    QuestionSerializer
)
from rest_framework.generics import ListAPIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class SubjectView(APIView):

    def get(self, request, format=None):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)

        return Response(serializer.data)


class SubjectQuestionList(APIView, PageNumberPagination):

     page_size = 20

     def get(self, request, pk):
         if request.GET['lang'] == 'ru_lang':
             lang = request.GET['lang']
             questions = Question.objects.filter(name__pk=pk).all().values('id', lang)
             result = self.paginate_queryset(questions, request, view=self)
             serializer = QuestionRuSerializer(result, many=True)
         elif request.GET['lang'] == 'en_lang':

             lang = request.GET['lang']
             questions = Question.objects.filter(name__pk=pk).all().values('id', lang)
             result = self.paginate_queryset(questions, request, view=self)
             serializer = QuestionEnSerializer(result, many=True)

         return self.get_paginated_response(serializer.data)


class SubjectQuestionDetail(APIView):

    def get_object(self, request, pk):
        print('<<<<<< hello world 1 >>>>>>')
        try:
            return Question.objects.get(pk=pk)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        print('<<<<<< hello world 2 >>>>>>')
        queryset = self.get_object(self, pk)
        serializer = QuestionSerializer(queryset)
        return Response(serializer.data)
