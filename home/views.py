from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .dlib import forImport_recognize_faces_image
import cv2

# Create your views here.
def index(request):

    #return HttpResponse("<p>Hello world!</p>")
    return render(request,'index.html')
    
def gallery(request):
    return render(request,'gallery.html')

def styletransfer(request):
    if request.method =='POST' and request.FILES['photoupload']:
        myfile=request.FILES['photoupload']
        fs = FileSystemStorage(location='home/static/images/')
        fs.save(myfile.name,myfile)
        # print(f'home/static/images/{myfile.name}.jpg')
        forImport_recognize_faces_image.readPara("home/dlib/encoding3.pickle",f'home/static/images/{myfile.name}','cnn')
        photopath="images/upload.jpg"

    return render(request,'styletransfer.html',locals())


def delmypic(request):
    return render(request,'delmypic.html')

def result(request):
    # if request.method =='POST':
    return render(request,'result.html',locals())