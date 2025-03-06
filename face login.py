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
    try:
        cam = cv2.VideoCapture(0) 
        face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        if not cam.isOpened():
            messagebox.showerror("Error", "Camera not detected!")
            return

        # Get latest image file
        training_path = 'C:\\Users\\Deepanshu\\Documents\\python\\project\\TrainingImage\\'
        list_of_files = glob.glob(training_path + '*') 

        if list_of_files:
            latest_file = max(list_of_files, key=os.path.getctime)
            name = os.path.splitext(os.path.basename(latest_file))[0]
            name = int(name) + 1
        else:
            name = 1  # First image name

        face_detected = False
        while not face_detected:
            ret, img = cam.read()
            if not ret:
                messagebox.showerror("Error", "Failed to capture image!")
                return

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                face_detected = True
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                face_img_path = os.path.join(training_path, f"{name}.jpg")
                cv2.imwrite(face_img_path, img[y:y+h, x:x+w])

            cv2.imshow('Face Capture', img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

        # User Input (Make sure text & text2 are defined in your UI)
        user = text.get()
        password = text2.get()

        # Database Connection
        try:
            conn = pymysql.connect(host='localhost', user='root', password='********', db='database')
            a = conn.cursor()
            a.execute("SELECT * FROM login WHERE Username=%s AND Password=%s", (user, password))
            result = a.fetchall()
            count = a.rowcount

            if count > 0:
                messagebox.showinfo("Success", "Login Successful!")
                win.destroy()
                subprocess.run(["python", "login2.py"])
            else:
                messagebox.showerror("Error", "Invalid Credentials! Try again.")

            conn.close()
        except pymysql.MySQLError as e:
            messagebox.showerror("Database Error", str(e))

    except Exception as e:
        messagebox.showerror("Error", str(e))
    

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
en2=Entry(lin,textvariable=c,show='*')
en2.grid(row=2,column=1,padx=10,pady=10)
btn=Button(lin,text="Login",bd=5,relief="raised",command=login,font=10)
btn.grid(row=3,column=1,padx=15,pady=15)
first.mainloop()
