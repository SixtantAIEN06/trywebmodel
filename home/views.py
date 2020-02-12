from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from .dlib import forImport_recognize_faces_image
from .BeautyGAN import main as BeautyGAN
from .BeautyGAN import split as beautysplit
import cv2
import glob
import os
# import subprocess
import tensorflow as tf

from .flask.peeweetest import Classified

from .object_detection.evaluate import YoloTest
YoloTest = YoloTest()

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
        # forImport_recognize_faces_image.readPara("home/dlib/encoding3.pickle",f'home/static/images/{myfile.name}','cnn')
        BeautyGAN.beauty(f'home/static/images/{myfile.name}')
        makeups = glob.glob(os.path.join('home','static','makeupstyle','*'))
        photopaths=[]
        for i in range(len(makeups)):
            photopaths.append(f"makeupstyle/{i+1}.jpg")
        print(photopaths)

        return redirect("/styletransfer2")

    return render(request,'styletransfer.html',locals())
    
def styletransfer2(request):
    if request.method =='POST' and request.POST["style"]:

        beautysplit.split(request.POST["style"])
        makeups = glob.glob(os.path.join('home','static','makeupstyle','*'))
        photopath="./home/static/temp/split.jpg"

    # elif os.path('./home/static/temp/split.jpg'):
    #     os.remove('./home/static/temp/split.jpg')  
    

    return render(request,'styletransfer2.html',locals())  
        

def objectdetection(request):
    if request.method =='POST' and request.FILES['photoupload']:
        myfile=request.FILES['photoupload']
        fs = FileSystemStorage(location='home/static/images/')
        fs.save(myfile.name,myfile)
        # print(f'home/static/images/{myfile.name}.jpg')
        # forImport_recognize_faces_image.readPara("home/dlib/encoding3.pickle",f'home/static/images/{myfile.name}','cnn')
        # photopath="images/upload.jpg"
        YoloTest.evaluate()
        print(YoloTest.dlist)
        for item in YoloTest.dlist:
            sort = Classified(**item) 
            sort.save()
    return render(request,'objectdetection.html',locals())


def delmypic(request):
    return render(request,'delmypic.html')

def result(request):
    # if request.method =='POST':
    return render(request,'result.html',locals())