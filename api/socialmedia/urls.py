from django.urls import path
from .views import CSVUploadView

app_name = 'socialmedia'

urlpatterns = [
    path('csvupload/', CSVUploadView.as_view(), name='csvupload'),
]