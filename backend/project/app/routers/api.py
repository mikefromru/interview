from django.urls import path
from .. views import api_views
# from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register(r'', api_views.SubjectQuestionDetail, basename='que')

api_urlpatterns = [
    path('subjects/', api_views.SubjectView.as_view()),
    path('subject/<pk>/', api_views.SubjectQuestionList.as_view()),
    path('subject/question/detail/<pk>/', api_views.SubjectQuestionDetail.as_view()),
    # path('subject/<pk>/', api_views.SubjectQuestionDetail.as_view()),
]

# api_urlpatterns += router.urls
