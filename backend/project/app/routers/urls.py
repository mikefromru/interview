from django.urls import path
from .. views import views

urlpatterns = [
    path('', views.SubjectListView.as_view(), name='list-subjects'),
]

