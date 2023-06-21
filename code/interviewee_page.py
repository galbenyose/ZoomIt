from tkinter import *
from interviewer_page import *
from users_data_base import *
import WaitForCall
import threading


def wait_for_server_to_create_a_call(ip: str,interviewee_name: str):
    sock = WaitForCall.WaitForCall(ip)
    manager = sock.wait_for_connection()
    answer = messagebox.askyesno("ZoomIt", f"{manager['FIRST_NAME']} wants to chat with you, do you accept?")
    print(answer)
    if answer is True:
        sock.accept_conversation()
        ip_interviewer=manager["IP_INTERVIEWER"]
        converstion_page_design(ip_interviewer,interviewee_name)
    else:
        sock.reject_conversation()
    return

def receive_frames_and_update_tkinter(root: Tk, client: CallClient):
    while True:
        filename = client.receive_frames()
        img = Image.open(filename)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
        imgtk= ImageTk.PhotoImage(image=img)
        lable=Label(root)
        lable.configure(image=imgtk)
        root.update()

def converstion_page_design(ip,interviewee_name):
        root = Tk()
        root.title("ZOOM IT")
        root.configure(bg="black")
        client = CallClient(ip)
        # Create and start the threads
        #receive_audio
        status=True
        def changestatus():
           status=False
        while status==True:
            receive_audio_thread = threading.Thread(target=client.receive_audio)
            receive_audio_thread.start()
            send_video_thread=threading.Thread(target=client.send_audio)
            send_video_thread.start()
            send_audio_thread=threading.Thread(target=client.send_frames)
            send_audio_thread.start()
            send_audio_thread=threading.Thread(target=receive_frames_and_update_tkinter, args=(root, client))
            send_audio_thread.start()
            exit_button=Button(root,text="EXIT",command= changestatus)
            exit_button.grid(row=200, column=1)
            root.mainloop()
        
        root.destroy()
        interviewee_design_page(interviewee_name)


def interviewee_design_page(name: str, ip: str):
    thread = threading.Thread(target=wait_for_server_to_create_a_call, args=(ip,name))
    thread.start()
    root=Tk()
    root.title("ZOOM IT")
    root.iconbitmap(r"images\logo.png.png")
    root.configure(bg="#F4F6F7")
    root.geometry("500x500")
    label1=Label(root,text="Hello "+ name,fg="black",bg="#F4F6F7",font=("verdana",20)).place(x=500,y=120)   
    def updat_user_passw():
        update_passw()
    def calls_frame():
        calls_requsts(root,"")
    fram_c= Button(root,text="call requsests",font=("verdana",25),command=calls_frame)
    fram_c.place(x=1150,y=200)
    updat_password=Button(root,text="updat password",font=("verdana",25),command=updat_user_passw)
    updat_password.place(x=1150,y=300)
    def Exit_page():
        root.destroy()
        thread.join()
        return True
        
        #למצוא דרך לחזור לדף ראשי
        
    disconnection=Button(root,text="disconnection",font=("verdana",25),command=Exit_page)
    disconnection.place(x=1150,y=500)
    root.mainloop()

# to take update password from intervies_page and disconnection

def calls_requsts(root,data):
    #creating call requstss in fram in interviewee page and gives him the abilty to refuse and exept the call
    frame_calls= LabelFrame(root,text="List of call requests",padx=50,pady=150)
    frame_calls.grid(padx=30,pady=300)
    label_calls= Label(frame_calls,text="your call requests:",font=("verdana",15))
    label_calls.grid(row=0,column=0)
    i=1
    def Exit():
        frame_calls.destroy()
    exit_button= Button(frame_calls,text='Exit',command=Exit)
    exit_button.grid(row=2, column=0)
    def confirmation():
        pass
    def refusal():
        pass
    while True:
        exit_button.grid(row=i+2, column=0)
        Label(frame_calls,text=data[0])
        Label.grid(row=i,column=0)
        Label(frame_calls,text=", "+data[1])
        Label.grid(row=i,column=1)
        Button(frame_calls,text="Call entry confirmation")
        Button.grid(row=i+2,column=0)
        Button(frame_calls,text="Refusal")
        Button.grid(row=i+2,column=1)
        i+=2        
   
    




# בקשת כניסה לשיחה?
# תיבת הזמנות לשיחה
