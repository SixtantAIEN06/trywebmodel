# -*- coding: utf-8 -*-

import tensorflow as tf
import numpy as np
import os
import glob
from imageio import imread, imsave
import cv2
import argparse
from PIL import Image


def preprocess(img):
    return (img / 255. - 0.5) * 2

def deprocess(img):
    return (img + 1) / 2

def beauty(image):
    org_h,org_w,_=imread(image).shape

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
# Read the input image
    img = cv2.imread(image)
    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    # Draw rectangle around the faces
    face_num=1
    for (x, y, w, h) in faces:
    # img = cv2.imread(args.no_makeup)

    # cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 0)
        print(x,y,w,h)
        im1 = img[y:y+h,x:x+w,::-1]


        # Display the output
        imsave(f'im{face_num}.jpg', im1)

        

        batch_size = 1
        img_size = 256
        no_makeup = cv2.resize(imread(f'im{face_num}.jpg'), (img_size, img_size))
        X_img = np.expand_dims(preprocess(no_makeup), 0)
        makeups = glob.glob(os.path.join('imgs', 'makeup', '*.*'))
        result = np.ones((img_size, (len(makeups) + 1) * img_size, 3))
        result[:img_size, :img_size] = no_makeup / 255.
        final=np.ones((org_h, (len(makeups) + 1) * org_w, 3))

        tf.reset_default_graph()
        sess = tf.Session()
        sess.run(tf.global_variables_initializer())

        saver = tf.train.import_meta_graph(os.path.join('model', 'model.meta'))
        saver.restore(sess, tf.train.latest_checkpoint('model'))

        graph = tf.get_default_graph()
        X = graph.get_tensor_by_name('X:0')
        Y = graph.get_tensor_by_name('Y:0')
        Xs = graph.get_tensor_by_name('generator/xs:0')

        for i in range(len(makeups)):
            makeup = cv2.resize(imread(makeups[i]), (img_size, img_size))
            Y_img = np.expand_dims(preprocess(makeup), 0)
            Xs_ = sess.run(Xs, feed_dict={X: X_img, Y: Y_img})
            Xs_ = deprocess(Xs_)
            final[:org_h,(i + 1) *org_w :(i + 2) *org_w] = img 
            

            # result[:img_size, (i + 1) * img_size: (i + 2) * img_size] = makeup / 255.
            result[:img_size, (i + 1) * img_size: (i + 2) * img_size] = Xs_[0]
            
        imsave('result_.jpg', result)
        result_ = cv2.resize(imread('result_.jpg'), (w*(len(makeups) + 1) , h))

        imsave('result_.jpg', result_)
        # result_=Image.open('result_.jpg')
        im_cut=[]
        final=final[:,:,::-1]
        if face_num==1:
            for i in range(len(makeups)):
                # print(i*w,0, (i+1)*w, h)
                final[y:y+h , x+(i+1)*org_w : x+w+(i+1)*org_w]=result_[:h,(i+1)*w:(i+2)*w]
            imsave('result.jpg', final)
        else:
            final=cv2.imread('result.jpg')[:,:,::-1]
            for i in range(len(makeups)):
                # print(i*w,0, (i+1)*w, h)
                final[y:y+h , x+(i+1)*org_w : x+w+(i+1)*org_w]=result_[:h,(i+1)*w:(i+2)*w]
            imsave('result.jpg', final)        
            

        os.remove(f'im{face_num}.jpg')

        face_num+=1

    os.remove('result_.jpg')


if __name__=="__main__":
    beauty("3.jpg")