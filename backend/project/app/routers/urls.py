from django.urls import path
from .. views import myadmin_views

urlpatterns = [
    # Myadmin
    path('', myadmin_views.SubjectListView.as_view(), name='list-subjects'),
    path('detail/<int:id>/<str:lang>/', myadmin_views.SubjectDetailView.as_view(), name='detail-subjects'),
]

