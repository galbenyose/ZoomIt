from tkinter import *
from tkinter import messagebox
from users_data_base import *
import interviewer_page
import interviewee_page
from clients import *


client = User('192.168.101.131', 1337)


def home_page_design():
#the design of the first page.
#the page containing user data entry box, information button and sign up button that alloes the user to move to other 
#page with ather relevent content
    root =Tk()
    root.title("ZOOM IT")
    root.configure(bg="#F4F6F7")
    root.geometry("500x500")
    site_name=Label(root, text="ZOOM IT",fg="black",bg="#F4F6F7",font=("verdana",50)).place(x=600,y=30)
    label1= Label(root, text="Hellow Walcom To Zoom It!!",fg="black",bg="#F4F6F7",font=("verdana",20)).place(x=500,y=120)
    information_b=Button(root, text= "information about us",command= information_button,font=("verdana",25))
    information_b.place(x=1100,y=500)
    sign_b=Button(root,text="sign up",font=("verdana",25),command=sign_up)
    sign_b.place(x=1150,y=400)
    fram_sign_up=LabelFrame(root,text="sign in",padx=50,pady=100)
    fram_sign_up.grid(padx=30,pady=300)
    user_name= Label(fram_sign_up,text="Username")
    user_name.grid(row=0,column=1)
    username = Entry(fram_sign_up,width=50,fg="black")
    username.grid(row=2,column=1)
    password =Label(fram_sign_up,text="Password")
    password.grid(row=8,column=1)
    user_password= Entry(fram_sign_up,width=50,fg="black")
    user_password.grid(row=10,column=1)
    
    def Delete():
        username.delete(0,END) 
        user_password.delete(0,END)
        
    def login():
        username_u=username.get()
        password_u=user_password.get()
        Delete()
        #ריצה על הטבלה והכנסת משתמש
        print(password_u)
        response = client.login(username_u,password_u)
        print("--------1")
        if response==False:
            error_masage= Label(fram_sign_up,text="one or two of your login details are incorrect ")
            error_masage.grid(row=16,column=1)
            error_masage2= Label(fram_sign_up,text="try again :) ")
            error_masage2.grid(row=17,column=1)
        
        elif int(response['TYPE'])==1:
            root.destroy()
            #להכניס ip עדכני
            while interviewer_page.interviewed_design_page!=True:
              interviewer_page.interviewed_design_page(response['FIRST_NAME'], client)
            home_page_design()
        else:
            root.destroy()
            while interviewee_page.interviewee_design_page!=True:
               interviewee_page.interviewee_design_page(response['FIRST_NAME'], client.ip)
            home_page_design()
            
    delete_key=Button(fram_sign_up, text="Delete", command= Delete)
    delete_key.grid(row=12,column=1)
    send_button=Button(fram_sign_up, text="Send",command= login)
    send_button.grid(row=14,column=1)
    
    root.mainloop()


def information_button():
#the design of tha information page
#לתקן
   root = Toplevel()
   root.title("ZOOM IT")
   root.iconbitmap(r"images\logo.png.png")
   root.geometry("450x550")
   image= Image.open(r"images\Zoom_it.png")
   bg = ImageTk.PhotoImage(image)
   label1 = Button(root, image=bg)
   label1.pack()
   def Exit_page():
        root.destroy()
   page_exit= Button(root,text="EXIT",command=Exit_page)
   page_exit.grid(row=15,column=2)
   root.mainloop()

def sign_up():
#the design of the sign up page where the customer fills the information about himeself 
    global root
    root=Tk()
    root.title("ZOOM IT")
    #root.iconbitmap(r"images\logo.png.png")
    root.geometry("330x380")
    first_name=Label(root,text="First Name")
    first_name.grid(row=0,column=2)
    name = Entry(root,width=50,fg="black")
    name.grid(row=1,column=2)
    last_name =Label(root, text="Last Name")
    last_name.grid(row=2,column=2)
    lastname_u=Entry(root, width=50,fg="black")
    lastname_u.grid(row=3,column=2)
    user_name= Label(root,text="Username")
    user_name.grid(row=4,column=2)
    username_u = Entry(root,width=50,fg="black")
    username_u.grid(row=5,column=2)
    password =Label(root,text="Password")
    password.grid(row=6,column=2)
    user_password= Entry(root,width=50,fg="black")
    user_password.grid(row=7,column=2)
    user_mail= Label(root,text="Email")
    user_mail.grid(row=8,column=2)
    mail_u=Entry(root,width=50,fg="black")
    mail_u.grid(row=9,column=2)
    type_user=Label(root,text="User Type")
    type_user.grid(row=10,column=2)
    choise = StringVar()
    #Default setting to the choise button
    Radiobutton(root,text="interviewee",variable= choise,value="interviewee").grid(row=11,column=2)
    Radiobutton(root,text="interviewer", variable= choise,value="interviewer").grid(row=12,column=2)
    def insert():
        #creating action to the insert button inclode seting client in the Database
        #and deleting buttons value that roten by the client
        #using Delete action
        name_user= name.get()
        lastname_user=lastname_u.get()
        username_user=username_u.get()
        password_user=user_password.get()
        mail_user= mail_u.get()
        choise_user= choise.get()
        print(choise_user)
        if choise_user=='interviewer':
            #1=מנהל 
            #2=מרואיין
            userstate_end =1
        else:
            userstate_end =2

        response=client.sign_up(mail_user,password_user,username_user,lastname_user,userstate_end,name_user)
        if response['RESULT']==FALSE:
            if response['REASON']=='email':
                messagebox.showerror('Error!', 'the email you selected isn\'t avalible please choose anothe one')
                return 
            elif response['REASON']=='username':
                messagebox.showerror('Error!','the user name you selected isn\'t available please choose another one ')
                return
        else:
            messagebox.showinfo("Signed Up!", "Your info entered successfully")            
       
    def Exit_page():
        root.destroy()
        
    def Delete():
        #deleting the information from the buttons
        name.delete(0,END)
        lastname_u.delete(0,END)
        username_u.delete(0,END)
        user_password.delete(0,END)
        mail_u.delete(0,END)
        choise.set('interviewer')# לבדוק תקינות
   
    delete_key=Button(root, text="Delete", command= Delete)
    delete_key.grid(row=13,column=2)
    send_button=Button(root, text="Send",command= insert)
    send_button.grid(row=14,column=2)
    page_exit= Button(root,text="EXIT",command=Exit_page)
    page_exit.grid(row=15,column=2)
    root.mainloop()

if __name__ == '__main__':
    home_page_design()