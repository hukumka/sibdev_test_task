from django.urls import path

from . import views

urlpatterns = [
    path('process_deals', views.process_deals),
    path('get_processing_result', views.get_processing_result),
]