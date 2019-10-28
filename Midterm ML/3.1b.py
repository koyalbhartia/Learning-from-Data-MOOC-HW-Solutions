#
#  Copyright 2019 Koyal Bhartia
#  @file    Semi-Cicle.py
#  @author  Koyal Bhartia
#  @date    03/30/2019
#  @version 1.0
#
#  @brief This is the code for Problem 3.1b from "Learning from Data"
#
#Import statments
import argparse
import numpy as np
import os, sys
from numpy import linalg as LA
import math
import pickle
import matplotlib.pyplot as plt
import random

def generate_data():
    c1in=0
    c1out=0
    c2in=0
    c2out=0

    X_data=np.column_stack((np.ones(N),np.ones(N)))
    fx=np.zeros((N))

    count1=0
    count2=0
    index=0
    while(count1<=999 or count2<=999):
            x1=random.uniform(-maxhori/2,maxhori/2)
            x2=random.uniform(-maxverti/2,maxverti/2)

            c1out=math.pow(x1,2)+math.pow(x2,2)-math.pow(rad+thk,2)
            c1in=math.pow(x1,2)+math.pow(x2,2)-math.pow(rad,2)

            c2in=math.pow(x1-(rad+thk/2),2)+math.pow(x2+sep,2)-math.pow(rad,2)
            c2out=math.pow(x1-(rad+thk/2),2)+math.pow(x2+sep,2)-math.pow(rad+thk,2)

            if(x2>=0 and c1in>=0 and c1out<=0 and count1<=999):
                X_data[index,0]=x1
                X_data[index,1]=x2
                a=index
                fx[index]=-1
                count1+=1
                index+=1
                plt.plot(x1,x2,'*r')
            if(x2+sep<=0 and c2in>=0 and c2out<=0 and count2<=999):
                X_data[index,0]=x1
                X_data[index,1]=x2
                b=index
                fx[index]=+1
                count2+=1
                index+=1
                plt.plot(x1,x2,'*b')

    plt.plot(X_data[a,0],X_data[a,1],'*r', label='y=-1 points')
    plt.plot(X_data[b,0],X_data[b,1],'*b', label='y=+1 points')
    return X_data,fx

def signCheck(num):
    if (num>0):
        return 1
    else:
        return -1

def misclassified(X_data,fx,w):
    break_point=1
    misclassify=[]
    X=np.column_stack((np.ones(len(X_data),dtype=int),X_data[:,0],X_data[:,1]))
    for i in range(0,len(X)):
        mul=np.matmul(w,X.transpose())
        sign=signCheck((mul[0,i]))
        if(sign!=(fx[i])):
            misclassify=np.append([misclassify],[i])
    if(len(misclassify)==0):
        break_point = 0
        a=-5
        length=0
    if(break_point == 1):
        point=random.randint(1,len(misclassify))
        a=int(misclassify[point-1])
    print("Misclas. pts count",len(misclassify))
    length=len(misclassify)
    return a,break_point,length,mul

def PLA():
    mis_counter=0
    mis_avg=0
    count=0
    break_point=1
    X_data,fx=generate_data()
    X=np.column_stack((np.ones(len(X_data),dtype=int),X_data[:,0],X_data[:,1]))
    w0=np.matmul(np.transpose(X),X)
    w1=LA.inv(w0)
    w2=np.matmul(w1,np.transpose(X))
    w3=np.matmul(w2,fx)
    w=np.array([w3])
    count=0
    while(break_point==1 and count<1000):
        count=count+1
        print("Iterations count:",count)
        pos,break_point,length,mul=misclassified(X_data,fx,w)
        if(pos!=-5):
            w_new=np.mat([0,0,0])
            w_new= w + fx[pos]*X[pos,:]
            #print(w_new)
            w=w_new
            print(w_new)
            #print("shape",np.shape(w_new))
            m=float(-w_new[0,1]/w_new[0,2])
            c=float(-w_new[0,0]/w_new[0,2])
            x_line1=np.mat([[-100],[100]])
            y_line1=m*x_line1+c
            plt.plot(x_line1,y_line1,'-c')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.axis([-maxhori/2,maxhori/2,-maxverti/2,maxverti/2])
            plt.title('Data set')
    if count==1:
        w_new=w
    return w_new

if __name__ == '__main__':

    centerx1,centerx2=0,0
    rad=10
    thk=5
    sep=5
    Total=2000
    Class=1000
    N=2000
    leftfit=rad+thk+1
    rightfit=rad+(thk)/2+rad+thk+1
    downfit=sep+rad+thk+1
    upfit=rad+thk+1
    maxhori=4*(rad+thk)
    maxverti=2*(rad+thk+sep)

    w_new=PLA()
    m=float(-w_new[0,1]/w_new[0,2])
    c=float(-w_new[0,0]/w_new[0,2])
    x_line1=np.mat([[-100],[100]])
    y_line1=m*x_line1+c
    #x_linet=x_line1
    #y_linet=t_slope*x_linet+t_intercept
    plt.plot(x_line1,y_line1,'-c',label='PLA Lines')
    plt.plot(x_line1,y_line1,'-b',label='Best Fit Line')
    #plt.plot(x_linet,y_linet,'-m',label='target_function')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.axis([-maxhori/2,maxhori/2+thk,-maxverti/2-sep,maxverti/2])
    plt.title('Data set')
    plt.legend()
    plt.show()
