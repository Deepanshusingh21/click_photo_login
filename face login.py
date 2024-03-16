from tkinter import*
from tkinter import messagebox
import pymysql
import pymysql.cursors
import cv2,os
import glob
import numpy as np
first=Tk()
first.config(bg="light blue")
first.geometry("350x300")
first.title("Welcome to the main page")
def login():
    cam = cv2.VideoCapture(0)
    face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #file name read
    list_of_files = glob.glob('C:\\Users\\Deepanshu\\Documents\\python\\TrainingImage\\*') 
    latest_file = max(list_of_files, key=os.path.getctime)
    name=os.path.basename(latest_file)
    name=os.path.splitext(name)[0]
    name=int(name)
    name=name+1
      
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(img,1.3,5)

        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
            #saving the captured face in the dataset folder TrainingImage
            cv2.imwrite("TrainingImage\ "+str(name) + ".jpg", img[y:y+h,x:x+w])
            #display the frame
            #cv2.imshow('frame',img)
            #wait for 100 miliseconds 
        if cv2.waitKey(5)  :
            break
            # break if the sample number is morethan 100
        elif sampleNum>=2:
            break
    cam.release()
    cv2.destroyAllWindows() 
    user=b.get()
    passwor=c.get()
    conn=pymysql.connect(host='localhost',user='root',password='Ankita@18',db='deepanshu')
    a=conn.cursor()
    a.execute("select * from login where username='"+user+"'and Password='"+passwor+"'")
    result=a.fetchall()
    count=a.rowcount
    if(count>0):
        messagebox.showinfo("message"," login")

    else:
        messagebox.showerror("message","not login")
    

lb=Label(first,text="Login",font=15,width=30,bd=5,relief="raised",fg="black")
lb.grid(row=0,column=0,padx=5,pady=5)
lin=Frame(first,width=500,height=500,bd=10,relief="raised")
lin.place(x=30,y=50)
lb1=Label(lin,font=10,text="Username")
lb1.grid(row=1,column=0,padx=10,pady=10)
lb2=Label(lin,text="Password",font=10)
lb2.grid(row=2,column=0,padx=10,pady=10)
b=StringVar()
en=Entry(lin,textvariable=b)
en.grid(row=1,column=1,padx=10,pady=10)
c=StringVar()
en2=Entry(lin,textvariable=c)
en2.grid(row=2,column=1,padx=10,pady=10)
btn=Button(lin,text="Login",bd=5,relief="raised",command=login,font=10)
btn.grid(row=3,column=1,padx=15,pady=15)
first.mainloop()
