

# api/urls.py
from django.urls import path
from .views import PredictCropView


urlpatterns = [
    path('predict/', PredictCropView.as_view()),
    path('predict', PredictCropView.as_view(), name='predict_crop'),

]
