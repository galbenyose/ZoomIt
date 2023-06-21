from tkinter import *
from tkinter import messagebox
from users_data_base import *
import socket
from clients import *
import threading


def interviewed_design_page(name, client):
    global root
    root=Tk()
    root.title("ZOOM IT")
    root.iconbitmap(r"images\logo.png.png")
    root.configure(bg="#F4F6F7")
    root.geometry("500x500")
    label1=Label(root,text="Hello "+ name,fg="black",bg="#F4F6F7",font=("verdana",20)).place(x=500,y=120)
    updat_password=Button(root,text="update password",font=("verdana",25),command=update_passw)
    updat_password.place(x=1150,y=300)
    
    def button_create_conversation():
        create_conversations(client)
    creat_conversation=Button(root,text="create conversation",font=("verdana",25), command=button_create_conversation )
    creat_conversation.place(x=1150,y=400)
    call_lists=Button(root, text= "lists of calls information",font=("verdana",25), command=list_of_connected_people)
    call_lists.place(x=1100,y=600)
    def Exit_page():
        root.destroy()
        return True
        #למצוא דרך לחזור לדף ראשי
    disconnection=Button(root,text="disconnection",font=("verdana",25),command=Exit_page)
    disconnection.place(x=1150,y=700)
    root.mainloop()


def list_of_connected_people():  # TODO fix db usage in client
    db=ZoomItDB()
    db._open()
    lst_connect_user_name=db.conected_people_username('users_u')
    lst_connect_firstname= db.conected_people_firstname('users_u')
    fram=LabelFrame(root,text="list of connected people")
    fram.grid(padx=100,pady=300)
    lablefram=Label(fram,text="the user name and the first name of the people that are connected to the site:")
    lablefram.grid(row=0,column=0)
    list_text_username=Text(fram,height=10, width=15)
    list_text_username.grid(row=1,column=0)
    list_text_first_name=Text(fram,height=10, width=15)
    list_text_first_name.grid(row=2,column=0)
    for con in lst_connect_user_name:
        list_text_username.insert(END,con+ ' \n')
    for con in lst_connect_firstname:
        list_text_first_name.insert(END,con+' \n')

    def Exit():
        fram.destroy()
    exit_button= Button(fram,text='Exit',command=Exit)
    exit_button.grid(row=7, column=0)

def list_calls():
    pass

def create_conversations(user: User):
    fram= LabelFrame(root,text="creat conversation",padx=50,pady=100)
    fram.grid(padx=30,pady=300)
    email_u= Label(fram,text="write your mail",font=("verdana",15))
    email_u.grid(row=0,column=1)
    email=Entry(fram, width=20,fg="black")
    email.grid(row=2,column=1)
    interviewee_name= Label(fram,text="write the username of the interviewer you want to talk to",font=("verdana",15))
    interviewee_name.grid(row=3,column=1)
    interviewee_username=Entry(fram, width=20,fg="black")
    interviewee_username.grid(row=4,column=1)
    name_interviewee=Label(fram,text="write the first name of the interviwee")
    name_interviewee.grid(row=5,column=1)
    interviewee=Entry(fram,width=20,fg="black")
    interviewee.grid(row=6,column=1)
    first_name=Label(fram,text="write your first name ")
    first_name.grid(row=7,column=1)
    name_interviewer=Entry(fram,width=20,fg="black")
    name_interviewer.grid(row=8,column=1)
    def send():
        username=interviewee_username.get()
        interviewer_email = email.get()
        interviewee_first_name= interviewee.get()
        firstname_interviewer=name_interviewer.get()
        responce=user.creatconvesation(interviewer_email,username)
        if responce is False:
            messagebox.showinfo("interviewee responce","the interviewee refused the call request")
            return
        else:
          ip_interviewee=responce["IP"]
          root.destroy()
          while True:
            converstion_page_design(ip_interviewee,12345,interviewee_first_name,firstname_interviewer,interviewer_email)
          #interviewed_design_page()
        
          
    def Delete():
        email.delete(0,END)
        interviewee_username.delete(0,END)
    def Exit():
        fram.destroy()
    delete_key=Button(fram, text="Delete", command= Delete)
    delete_key.grid(row=5,column=1)
    send_button=Button(fram, text="Send",command=send)
    send_button.grid(row=6, column=1)
    exit_button= Button(fram,text='Exit',command=Exit)
    exit_button.grid(row=7, column=1)
    
def receive_frames_and_update_tkinter(root: Tk, client: CallClient):
    while True:
        filename = client.receive_frames()
        img = Image.open(filename)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        imgtk= ImageTk.PhotoImage(image=img)
        lable = Label(root)
        lable.configure(image=imgtk)
        decode_image(img, client)
        root.update()
    

def decode_image(img, client: CallClient):
    responce=client.Face_decoding(img)
    if responce=="5.1":
        messagebox.showinfo("Face decoding","the interviewee thouched his nose \n he is lying or under pressure ")
    elif responce=="5.2":
        messagebox.showinfo("Face decoding","the interviewee thouched his mouth \n he lies/ feels remorse/ hides information/ ashamed ")
    elif responce=="5.3":
        messagebox.showinfo("Face decoding","the interviewee thouched his ear \n he is feeling uncomfortable")
    elif responce=="5.4":
        messagebox.showinfo(" Face decoding","the interviewee thouched his forehead \n he is thinking/ feels frustration or despair")
    elif responce=="5.5":
        messagebox.showinfo("Face decoding","the interviewee pursing the lips \n feeling dissatisfacrion ")

def converstion_page_design(ip,port,name_interviewee,interviewer_name,interviewed_email,):
    root = Tk()
    root.title("ZOOM IT")
    root.configure(bg="black")
    client= CallClient(ip)
    # Create and start the threads
    #receive_audio
    status=True
    exit_button=Button(root,text="EXIT",command=root.destroy)
    exit_button.grid(row=20, column=1)
    receive_audio_thread = threading.Thread(target=client.receive_audio)
    receive_audio_thread.start()
    send_video_thread=threading.Thread(target=client.send_audio)
    send_video_thread.start()
    send_audio_thread=threading.Thread(target=client.send_frames)
    send_audio_thread.start()
    send_audio_thread=threading.Thread(target=receive_frames_and_update_tkinter, args=(root, client,))
    send_audio_thread.start()
    root.mainloop()
    interviewed_design_page(interviewer_name)


def update_passw():
    fram= LabelFrame(root,text="Updat password",padx=50,pady=100)
    fram.grid(padx=30,pady=300)
    email_u= Label(fram,text="write your mail",font=("verdana",15))
    email_u.grid(row=0,column=1)
    email=Entry(fram, width=20,fg="black")
    email.grid(row=2,column=1)
    password= Label(fram,text="write your new password",font=("verdana",15))
    password.grid(row=3,column=1)
    new_passw=Entry(fram, width=20,fg="black")
    new_passw.grid(row=4,column=1)
    def update():
        passw= new_passw.get()
        email_user=email.get()
        client = User('127.0.0.1', 1234)
        response=client.change_password(passw,"users_u",email_user)
        if response[1]:
            messagebox.showinfo('Password Changed', 'The password has changed successfully')
            return
        messagebox.showerror('Error!', 'Password didn\'t change')
        return
    def Delete():
        email.delete(0,END)
        new_passw.delete(0,END)
    def Exit():
        fram.destroy()
    delete_key=Button(fram, text="Delete", command= Delete)
    delete_key.grid(row=5,column=1)
    send_button=Button(fram, text="Send",command=update)
    send_button.grid(row=6, column=1)
    exit_button= Button(fram,text='Exit',command=Exit)
    exit_button.grid(row=7, column=1)

    

#  פתיחת שיחה כוללת זימון לשיחה
# רשימת שיחה : כוללת סוגי התנהגות
# יצירת fram בו המראיין יכול להקליד שם של משתמש ולבדוק אם הוא מחובר 