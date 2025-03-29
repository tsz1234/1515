from django.urls import path
from myApp import views
urlpatterns = [
    path('screenData/', views.screenData,name='screenData'),
    path('summary/', views.summary, name='summary'),
    path('get_options/', views.get_options),
    path('predict_price/', views.predict_price,name='predict_price'),
]
