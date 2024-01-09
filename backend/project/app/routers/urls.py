from django.urls import path
from .. views import myadmin_views

urlpatterns = [
    # Myadmin
    path('', myadmin_views.SubjectListView.as_view(), name='list-subjects'),
    path('detail/<int:id>/<str:lang>/', myadmin_views.SubjectDetailView.as_view(), name='detail-subjects'),
    path('create-subject/', myadmin_views.SubjectCreateView.as_view(), name='create-subject'),
    path('delete-subject/<pk>/', myadmin_views.SubjectDeleteView.as_view(), name='delete-subject'),
    path('update-subject/<pk>/', myadmin_views.SubjectUpdateView.as_view(), name='update-subject'),
]

