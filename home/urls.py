from django.urls import path
from . import views
urlpatterns = [
    path('',views.index),
    path('gallery/',views.gallery),
    path('styletransfer/',views.styletransfer),
    path('delmypic/',views.delmypic,name='uplaodfile'),
    path('styletransfer/{imgpath:imgpath}',views.styletransfer),
    path('result/',views.result),
    path('objectdetection/',views.objectdetection),
]
