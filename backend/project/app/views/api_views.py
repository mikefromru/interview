from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from django.http import Http404
from .. models import Subject, Question
from .. serializers import (
    SubjectSerializer,
    QuestionEnSerializer,
    QuestionRuSerializer
)
from rest_framework.generics import ListAPIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class StandardResultsSetPagination(PageNumberPagination):

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    # def get_paginated_response(self, data):
    #     return Response({
    #         'next': self.get_next_link(),
    #         'previous': self.get_previous_link(),
    #         'count': self.page.paginator.count,
    #         'total_pages': self.page.paginator.num_pages,
    #         'results': data
    #     })


class SubjectView(APIView):

    def get(self, request, format=None):
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

class SubjectQuestionDetail(APIView):

    # queryset = Question.objects.all()
    pagination_class = StandardResultsSetPagination
    # serializer_class = QuestionEnSerializer

    @property
    def paginator(self):
        """The paginator instance associated with the view, or `None`."""
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """Return a single page of results, or `None` if pagination is disabled."""
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """Return a paginated style `Response` object for the given output data."""
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_object(self, pk, lang, answer):
        try:
            return Question.objects.filter(name__pk=pk).all().values(lang, answer)
        except Question.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        lang = request.GET['lang']
        answer = request.GET.get('answer')
        questions = self.get_object(pk, lang, answer)

        page = self.paginate_queryset(questions)

        if page is not None:
            if lang == 'en_lang':
                serializer = QuestionEnSerializer(page, many=True)
            elif lang == 'ru_lang':
                serializer = QuestionRuSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        if lang == 'en_lang':
            serializer = QuestionEnSerializer(questions, many=True)
        elif lang == 'ru_lang':
            serializer = QuestionRuSerializer(questions, many=True)

        return Response(serializer.data)
