from django.urls import path

from pereval.views import SubmitData, SubmitDetailData

urlpatterns = [
    path('api/v1/submitData/', SubmitData.as_view(), name='submitData'),
]