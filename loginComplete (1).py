from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
from tkinter.font import BOLD
import mysql.connector
import random
import time
import datetime

def main():
    win=Tk()
    app=Login_Window(win)
    win.mainloop()




class Login_Window:
    def __init__(self,root):
        self.root=root
        self.root.title("Login")
        self.root.geometry('1550x800+0+0')
        

        frame=Frame(self.root,bg="black")
        frame.place(x=500,y=140,width=340,height=450)

        get_str=Label(frame,text="Get Started",font=("times new roman",18,"bold"),fg="white",bg="black")
        get_str.place(x=115,y=100)

        #label
        username=lbl=Label(frame,text="Username",font=("times new roman",15,"bold"),fg="white",bg="black")
        username.place(x=70,y=155)

        self.txtuser=ttk.Entry(frame,font=("times new roman",15,"bold"))
        self.txtuser.place(x=40,y=180,width=270)

        password=lbl=Label(frame,text="Password",font=("times new roman",15,"bold"),fg="white",bg="black")
        password.place(x=70,y=225)

        self.txtpass=ttk.Entry(frame,font=("times new roman",15,"bold"),show="*")
        self.txtpass.place(x=40,y=250,width=270)

        loginbtn=Button(frame,command=self.login,text="Login",font=("times new roman",15,"bold"),bd=3,relief=RIDGE,fg="white",bg="red",activeforeground="white",activebackground="red")
        loginbtn.place(x=110,y=300,width=120,height=35)

        registerbtn=Button(frame,text="New User Register",command=self.register_window,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        registerbtn.place(x=15,y=350,width=160)

        registerbtn=Button(frame,text="Forget Password",command=self.forgot_password_window,font=("times new roman",10,"bold"),borderwidth=0,fg="white",bg="black",activeforeground="white",activebackground="black")
        registerbtn.place(x=10,y=370,width=160)




    def register_window(self):
        self.new_window=Toplevel(self.root)
        self.app=Register(self.new_window)

    def login(self):
        if self.txtuser.get()=="" or self.txtpass.get()=="":
            messagebox.showerror("Error","all field required")
        elif self.txtuser.get()=="shriya"and self.txtpass.get()=="saxena":
            messagebox.showinfo("Success","Welcome")
            self.new_window=Toplevel(self.root)
            self.app=Hospital(self.new_window)
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="sqlshriyawork1!",database="hospital")
            my_cursor=conn.cursor()
            my_cursor.execute("select * from register where emailid=%s and password=%s",(
                                                                                        self.txtuser.get(),
                                                                                        self.txtpass.get()
                                                                                     ))  
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Invalid Username or Password")
            else:
                open_main=messagebox.askyesno("YesNo","Access only Admin")
                if open_main>0:
                    self.new_window=Toplevel(self.root)
                    self.app=Hospital(self.new_window)
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()
    
    # ============================ RESET PASSWORD ===========================

    def reset(self):
        if self.combo_security_q.get()=="Select":
            messagebox.showerror("Error","Select the Security Question")
        elif self.txt_security_a.get()=="":
            messagebox.showerror("Error","Please enter the answer")
        elif self.txt_newpass.get()=="":
            messagebox.showerror("Error","Please enter the new password")
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="sqlshriyawork1!",database="hospital")
            my_cursor=conn.cursor()
            query=("select * from register where emailid=%s and security_question=%s and security_answer=%s")
            value=(self.txtuser.get(),self.combo_security_q.get(),self.txt_security_a.get())
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row==None:
                messagebox.showerror("Error","Please enter the correct answer")
            else:
                query=("update register set password=%s where emailid=%s")
                value=(self.txt_newpass.get(),self.txtuser.get())
                my_cursor.execute(query,value)

                conn.commit()
                conn.close()
                messagebox.showinfo("Info","Your password has been reset, please login using the new password",parent=self.root2)
                self.root2.destroy()
                


    # ========================== FORGOT PASSWORD WINDOW ======================

    def forgot_password_window(self):
        if self.txtuser.get()=="":
            messagebox.showerror("Error","Please write the email address to reset the password")
        else:
            conn=mysql.connector.connect(host="localhost",user="root",password="sqlshriyawork1!",database="hospital")
            my_cursor=conn.cursor()
            query=("select * from register where emailid=%s")
            value=(self.txtuser.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            #print(row)


            if row==None:
                messagebox.showerror("Error","Please enter a valid username")
            else:
                conn.close()
                self.root2=Toplevel()
                self.root2.title("Forgot Password")
                self.root2.geometry("340x450+610+170")


                l=Label(self.root2,text="Forgot Password",font=("times new roman",15,"bold"),fg="red",bg="white")
                l.place(x=0,y=10,relwidth=1)

                security_q=Label(self.root2,text="Select Security Questions",font=("times new roman",15,"bold"),bg="white",fg="black")
                security_q.place(x=50,y=80)

                self.combo_security_q=ttk.Combobox(self.root2,font=("times new roman",15,"bold"),state="readonly")
                self.combo_security_q["values"]=("Select","Your birth place","Your friend name","Your pet name")
                self.combo_security_q.place(x=50,y=110,width=250)
                self.combo_security_q.current(0)

                security_a=Label(self.root2,text="Security Answer",font=("times new roman",15,"bold"),bg="white",fg="black")
                security_a.place(x=50,y=150)

                self.txt_security_a=ttk.Entry(self.root2,font=("times new roman",15))
                self.txt_security_a.place(x=50,y=180,width=250)

                new_password=Label(self.root2,text="New Password",font=("times new roman",15,"bold"),bg="white",fg="black")
                new_password.place(x=50,y=220)

                self.txt_newpass=ttk.Entry(self.root2,font=("times new roman",15),show="*")
                self.txt_newpass.place(x=50,y=250,width=250)

                btn=Button(self.root2,text="Reset",command=self.reset,font=("times new roman",15,"bold"),fg="white",bg="green")
                btn.place(x=130,y=290)


class Register:
    def __init__(self,root):
        self.root=root
        self.root.title("Register")
        self.root.geometry('1600x900+0+0')

        #----------variables

        self.var_fname=StringVar()
        self.var_lname=StringVar()
        self.var_contact=StringVar()
        self.var_email=StringVar()
        self.var_securityq=StringVar()
        self.var_securitya=StringVar()
        self.var_pass=StringVar()
        self.var_confpass=StringVar()


        frame=Frame(self.root,bg="white")
        frame.place(x=280,y=80,width=800,height=550)

        #----------register

        register_lbl=Label(frame,text="REGISTER HERE",font=("times new roman",20,"bold"),fg="darkgreen",bg="white")
        register_lbl.place(x=20,y=20)

        #---------------row 1

        fname=Label(frame,text="FIRST NAME",font=("times new roman",15,"bold"),bg="white")
        fname.place(x=50,y=100)

        self.fname_entry=ttk.Entry(frame,textvariable=self.var_fname,font=("times new roman",15))
        self.fname_entry.place(x=50,y=130,width=250)

        l_name=Label(frame,text="LAST NAME",font=("times new roman",15,"bold"),bg="white")
        l_name.place(x=370,y=100)

        self.txt_lname=ttk.Entry(frame,textvariable=self.var_lname,font=("times new roman",15))
        self.txt_lname.place(x=370,y=130,width=250)

        #-------------row2

        contact=Label(frame,text="Contact No",font=("times new roman",15,"bold"),bg="white",fg="black")
        contact.place(x=50,y=170)

        self.txt_contact=ttk.Entry(frame,textvariable=self.var_contact,font=("times new roman",15))
        self.txt_contact.place(x=50,y=200,width=250)

        email=Label(frame,text="Email",font=("times new roman",15,"bold"),bg="white",fg="black")
        email.place(x=370,y=170)

        self.txt_email=ttk.Entry(frame,textvariable=self.var_email,font=("times new roman",15))
        self.txt_email.place(x=370,y=200,width=250)

        #--------------row3

        security_q=Label(frame,text="Select Security Questions",font=("times new roman",15,"bold"),bg="white",fg="black")
        security_q.place(x=50,y=240)

        self.combo_security_q=ttk.Combobox(frame,textvariable=self.var_securityq,font=("times new roman",15,"bold"),state="readonly")
        self.combo_security_q["values"]=("Select","Your birth place","Your friend name","Your pet name")
        self.combo_security_q.place(x=50,y=270,width=250)
        self.combo_security_q.current(0)

        security_a=Label(frame,text="Security Answer",font=("times new roman",15,"bold"),bg="white",fg="black")
        security_a.place(x=370,y=240)

        self.txt_security_a=ttk.Entry(frame,textvariable=self.var_securitya,font=("times new roman",15))
        self.txt_security_a.place(x=370,y=270,width=250)

        #------------row4

        pswd=Label(frame,text="Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        pswd.place(x=50,y=310)

        self.txt_pswd=ttk.Entry(frame,textvariable=self.var_pass,font=("times new roman",15),show="*")
        self.txt_pswd.place(x=50,y=340,width=250)

        confirm_pswd=Label(frame,text="Confirm Password",font=("times new roman",15,"bold"),bg="white",fg="black")
        confirm_pswd.place(x=370,y=310)

        self.txt_confirm_pswd=ttk.Entry(frame,textvariable=self.var_confpass,font=("times new roman",15),show="*")
        self.txt_confirm_pswd.place(x=370,y=340,width=250)

        #======checkbutton
        self.var_check=IntVar()
        checkbtn=Checkbutton(frame,variable=self.var_check,text="I Agree the Terms and Conditions",font=("times new roman",12,"bold"),onvalue=1,offvalue=0)
        checkbtn.place(x=50,y=380)

        #---------buttons

        b2=Button(frame,command=self.register_data,borderwidth=0,cursor="hand2",font=("times new roman",15,"bold"),text="Register Now")
        b2.place(x=300,y=450,width=200)

        #========function declaration=======

    def register_data(self):
        if self.var_fname.get()==""or self.var_email.get()==""or self.var_securityq.get()=="Select":
            messagebox.showerror("Error","All fields are required")
        elif self.var_pass.get()!=self.var_confpass.get():
            messagebox.showerror("Error","Password and confirm password must be same")    
        elif self.var_check.get()==0:
            messagebox.showerror("Error","Please agree our terms and conditions")
        else: 
            conn=mysql.connector.connect(host="localhost",user="root",password="sqlshriyawork1!",database="hospital")
            my_cursor=conn.cursor()
            query=("select * from register where emailid =%s")
            value=(self.var_email.get(),)
            my_cursor.execute(query,value)
            row=my_cursor.fetchone()
            if row!=None:
                messagebox.showerror("Error","User already exits, please try another email")
            else:
                my_cursor.execute("Insert into register values(%s,%s,%s,%s,%s,%s,%s)",(
                                                                                        self.var_contact.get(),
                                                                                        self.var_lname.get(),
                                                                                        self.var_fname.get(),
                                                                                        self.var_email.get(),
                                                                                        self.var_securityq.get(),
                                                                                        self.var_securitya.get(),
                                                                                        self.var_pass.get()
                                                                                     ))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success","Registered Successfully")
  
class Hospital():
    def __init__(self,root):
        self.root=root
        self.root.title("Hospital Management System")
        self.root.geometry("1540x800+0+0")

        
        self.Nameoftablets=StringVar()
        self.ref=StringVar()
        self.Dose=StringVar()
        self.NumberofTablets=StringVar()
        self.Dr=StringVar()
        self.issuedate=StringVar()
        self.expdate=StringVar()
        self.Dailydose=StringVar()
        self.spo2=StringVar()
        self.sex=StringVar()
        self.bp=StringVar()
        self.age=StringVar()
        self.Medication=StringVar()
        self.patientid=StringVar()
        self.Weight=StringVar()
        self.PatientName=StringVar()
        self.dob=StringVar()
        self.patientaddress=StringVar()
        



        lbltitle=Label(self.root,bd=20,relief=RIDGE,text="+ HOSPITAL MANAGEMENT SYSTEM",fg="red",bg="white",font=("times new roman",50,BOLD))
        lbltitle.pack(side=TOP,fill=X)



        # ======================================= DATA FRAME ==================================================
        Dataframe=Frame(self.root,bd=20,relief=RIDGE)
        Dataframe.place(x=0,y=130,width=1530,height=400)


        DataframeLeft=LabelFrame(Dataframe,bd=10,relief=RIDGE,padx=10,font=("arial",12,BOLD),text="Patient Information")
        DataframeLeft.place(x=0,y=5,width=980,height=350)

        DataframeRight=LabelFrame(Dataframe,bd=10,relief=RIDGE,padx=10,font=("arial",12,BOLD),text="Prescription")
        DataframeRight.place(x=990,y=5,width=460,height=350)

        # ===================================== BUTTONS FRAME =======================================

        Buttonframe=Frame(self.root,bd=20,relief=RIDGE)
        Buttonframe.place(x=0,y=530,width=1530,height=70)

        # ===================================== DETAILS FRAME =======================================

        Detailsframe=Frame(self.root,bd=20,relief=RIDGE)
        Detailsframe.place(x=0,y=600,width=1530,height=190)

        # ======================================= Dataframe left =======================================

        lblNameTablet=Label(DataframeLeft,text="Names Of Tablet :",font=("arial",12,BOLD),padx=2,pady=6)
        lblNameTablet.grid(row=0,column=0)

        self.comNametablet=ttk.Combobox(DataframeLeft,textvariable=self.Nameoftablets,font=("arial",12,BOLD),width=33)
        self.comNametablet["values"]=("Nise","Corona Vaccine","Acetaminophen","Adderall","Amlodipe","Ativan")
        self.comNametablet.grid(row=0,column=1)

        lblref=Label(DataframeLeft,font=("arial",12,BOLD),text="Reference No.:",padx=2)
        lblref.grid(row=1,column=0,sticky=W)
        self.txtref=Entry(DataframeLeft,font=("arial",13,BOLD),textvariable=self.ref,width=35)
        self.txtref.grid(row=1,column=1)

        lblDose=Label(DataframeLeft,font=("arial",12,BOLD),text="Dose :",padx=2,pady=4)
        lblDose.grid(row=2,column=0,sticky=W)
        self.txtDose=Entry(DataframeLeft,font=("arial",13,BOLD),textvariable=self.Dose,width=35)
        self.txtDose.grid(row=2,column=1)

        lblNoOfTablets=Label(DataframeLeft,font=("arial",12,BOLD),text="No. of Tablets :",padx=2,pady=6)
        lblNoOfTablets.grid(row=3,column=0,sticky=W)
        self.txtNoOfTablets=Entry(DataframeLeft,font=("arial",13,BOLD),textvariable=self.NumberofTablets,width=35)
        self.txtNoOfTablets.grid(row=3,column=1)

        lblDr=Label(DataframeLeft,font=("arial",12,BOLD),text="Prescribed by Dr. :",padx=2,pady=6)
        lblDr.grid(row=4,column=0,sticky=W)
        self.txtDr=Entry(DataframeLeft,font=("arial",13,BOLD),textvariable=self.Dr,width=35)
        self.txtDr.grid(row=4,column=1)

        lblIssueDate=Label(DataframeLeft,font=("arial",12,BOLD),text="Issue Date :",padx=2,pady=6)
        lblIssueDate.grid(row=5,column=0,sticky=W)
        self.txtIssueDate=Entry(DataframeLeft,font=("arial",13,BOLD),textvariable=self.issuedate,width=35)
        self.txtIssueDate.grid(row=5,column=1)

        lblExpDate=Label(DataframeLeft,font=("arial",12,BOLD),text="Expiry Date :",padx=2,pady=6)
        lblExpDate.grid(row=6,column=0,sticky=W)
        self.txtExpDate=Entry(DataframeLeft,font=("arial",13,BOLD),textvariable=self.expdate,width=35)
        self.txtExpDate.grid(row=6,column=1)

        lblDailyDose=Label(DataframeLeft,font=("arial",12,BOLD),text="Daily Dose :",padx=2,pady=4)
        lblDailyDose.grid(row=7,column=0,sticky=W)
        self.txtDailyDose=Entry(DataframeLeft,font=("arial",13,BOLD),textvariable=self.Dailydose,width=35)
        self.txtDailyDose.grid(row=7,column=1)

        lblspo2=Label(DataframeLeft,font=("arial",12,BOLD),text="SpO2 :",padx=2,pady=6)
        lblspo2.grid(row=8,column=0,sticky=W)
        self.txtspo2=Entry(DataframeLeft,font=("arial",13,BOLD),textvariable=self.spo2,width=35)
        self.txtspo2.grid(row=8,column=1)

        lblsex=Label(DataframeLeft,font=("arial",12,BOLD),text="Sex :",padx=2)
        lblsex.grid(row=0,column=2,sticky=W)
        self.txtsex=Entry(DataframeLeft,font=("arial",13,BOLD),textvariable=self.sex,width=35)
        self.txtsex.grid(row=0,column=3)

        lblBloodPressure=Label(DataframeLeft,font=("arial",12,BOLD),text="Blood Pressure :",padx=2,pady=6)
        lblBloodPressure.grid(row=1,column=2,sticky=W)
        self.txtBloodPressure=Entry(DataframeLeft,font=("arial",13,BOLD),textvariable=self.bp,width=35)
        self.txtBloodPressure.grid(row=1,column=3)

        lblage=Label(DataframeLeft,font=("arial",12,BOLD),text="Age :",padx=2,pady=6)
        lblage.grid(row=2,column=2,sticky=W)
        self.txtage=Entry(DataframeLeft,font=("arial",12,BOLD),textvariable=self.age,width=35)
        self.txtage.grid(row=2,column=3)

        lblMedicine=Label(DataframeLeft,font=("arial",12,BOLD),text="Medication :",padx=2,pady=6)
        lblMedicine.grid(row=3,column=2,sticky=W)
        self.txtMedicine=Entry(DataframeLeft,font=("arial",12,BOLD),textvariable=self.Medication,width=35)
        self.txtMedicine.grid(row=3,column=3)

        lblPatientId=Label(DataframeLeft,font=("arial",12,BOLD),text="Patient Id :",padx=2,pady=6)
        lblPatientId.grid(row=4,column=2,sticky=W)
        self.txtPatientId=Entry(DataframeLeft,font=("arial",12,BOLD),textvariable=self.patientid,width=35)
        self.txtPatientId.grid(row=4,column=3)

        lblweight=Label(DataframeLeft,font=("arial",12,BOLD),text="Weight :",padx=2,pady=6)
        lblweight.grid(row=5,column=2,sticky=W)
        self.txtweight=Entry(DataframeLeft,font=("arial",12,BOLD),textvariable=self.Weight,width=35)
        self.txtweight.grid(row=5,column=3)


        lblPatientName=Label(DataframeLeft,font=("arial",12,BOLD),text="Patient Name :",padx=2,pady=6)
        lblPatientName.grid(row=6,column=2,sticky=W)
        self.txtPatientName=Entry(DataframeLeft,font=("arial",12,BOLD),textvariable=self.PatientName,width=35)
        self.txtPatientName.grid(row=6,column=3)

        lblDateOfBirth=Label(DataframeLeft,font=("arial",12,BOLD),text="Date Of Birth :",padx=2,pady=6)
        lblDateOfBirth.grid(row=7,column=2,sticky=W)
        self.txtDateOfBirth=Entry(DataframeLeft,font=("arial",12,BOLD),textvariable=self.dob,width=35)
        self.txtDateOfBirth.grid(row=7,column=3)
        
        lblPatientAddress=Label(DataframeLeft,font=("arial",12,BOLD),text="Patient Address :",padx=2,pady=6)
        lblPatientAddress.grid(row=8,column=2,sticky=W)
        self.txtPatientAddress=Entry(DataframeLeft,font=("arial",12,BOLD),textvariable=self.patientaddress,width=35)
        self.txtPatientAddress.grid(row=8,column=3)




        #=======================DataframeRight===================================
        self.txtPrescription=Text(DataframeRight,font=("arial",12,BOLD),width=45,height=16,padx=2,pady=6)
        self.txtPrescription.grid(row=0,column=0) 



        #========================Buttons===========================================
        img=Image.open(r"C:\Users\SHIA\Downloads\Prescription.jpeg")
        img=img.resize((250,30),Image.ANTIALIAS)
        self.photoimage1=ImageTk.PhotoImage(img)
        btnPrescription=Button(Buttonframe,command=self.iPrescription,image=self.photoimage1,cursor="hand2",borderwidth=0,pady=6,padx=2)
        btnPrescription.grid(row=0,column=0)

        img=Image.open(r"C:\Users\SHIA\Downloads\Prescriptiondata.jpeg")
        img=img.resize((300,30),Image.ANTIALIAS)
        self.photoimage2=ImageTk.PhotoImage(img)
        btnPrescriptionData=Button(Buttonframe,text="Prescription Data",command=self.iPrescriptiondata,cursor="hand2",borderwidth=0,image=self.photoimage2,padx=2,pady=6)
        btnPrescriptionData.grid(row=0,column=1)

        img=Image.open(r"C:\Users\SHIA\Downloads\Update.jpeg")
        img=img.resize((200,30),Image.ANTIALIAS)
        self.photoimage3=ImageTk.PhotoImage(img)
        btnUpdate=Button(Buttonframe,text="Update",cursor="hand2",command=self.update_data,image=self.photoimage3,borderwidth=0,padx=2,pady=6)
        btnUpdate.grid(row=0,column=2)

        img=Image.open(r"C:\Users\SHIA\Downloads\Delete.jpeg")
        img=img.resize((160,30),Image.ANTIALIAS)
        self.photoimage4=ImageTk.PhotoImage(img)
        btnDelete=Button(Buttonframe,text="Delete",command=self.idelete,cursor="hand2",image=self.photoimage4,borderwidth=0,padx=2,pady=6)
        btnDelete.grid(row=0,column=3)

        img=Image.open(r"C:\Users\SHIA\Downloads\Reset.jpeg")
        img=img.resize((180,30),Image.ANTIALIAS)
        self.photoimage5=ImageTk.PhotoImage(img)
        btnReset=Button(Buttonframe,text="Reset",command=self.clear,cursor="hand2",image=self.photoimage5,borderwidth=0,padx=2,pady=6)
        btnReset.grid(row=0,column=4)

        img=Image.open(r"C:\Users\SHIA\Downloads\Exit.jpeg")
        img=img.resize((220,30),Image.ANTIALIAS)
        self.photoimage6=ImageTk.PhotoImage(img)
        btnExit=Button(Buttonframe,text="Exit",command=self.iexit,cursor="hand2",image=self.photoimage6,borderwidth=0,padx=2,pady=6)
        btnExit.grid(row=0,column=5)

        #====================================Table============================
        #====================================scrollbar========================

        scroll_x=ttk.Scrollbar(Detailsframe,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(Detailsframe,orient=VERTICAL)
        self.hospital_table=ttk.Treeview(Detailsframe,column=("ref","nameoftablet","dose","nooftablet","Dr","issuedate",
                                "expdate","dailydose","spo2","sex","bp","age","medication","pid","wt","pname","dob","address"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)

        scroll_x.config(command=self.hospital_table.xview)
        scroll_y.config(command=self.hospital_table.yview)
        

        self.hospital_table.heading("ref",text="Reference No.")
        self.hospital_table.heading("nameoftablet",text="Name of Tablet")
        self.hospital_table.heading("dose",text="Dose")
        self.hospital_table.heading("nooftablet",text="No. of Tablets")
        self.hospital_table.heading("Dr",text="Prescribed by Dr.")
        self.hospital_table.heading("issuedate",text="Issue Date")
        self.hospital_table.heading("expdate",text="Expiry Date")
        self.hospital_table.heading("dailydose",text="Daily Dose")
        self.hospital_table.heading("spo2",text="SpO2")
        self.hospital_table.heading("sex",text="Sex")
        self.hospital_table.heading("bp",text="Blood Pressure")
        self.hospital_table.heading("age",text="Age")
        self.hospital_table.heading("medication",text="Medication")
        self.hospital_table.heading("pid",text="Patient Id")
        self.hospital_table.heading("wt",text="Weight")
        self.hospital_table.heading("pname",text="Patient Name")
        self.hospital_table.heading("dob",text="Date of Birth")
        self.hospital_table.heading("address",text="Address")

        self.hospital_table["show"]="headings"

        self.hospital_table.column("ref",width=100)
        self.hospital_table.column("nameoftablet",width=100)
        self.hospital_table.column("dose",width=100)
        self.hospital_table.column("nooftablet",width=100)
        self.hospital_table.column("Dr",width=100)
        self.hospital_table.column("issuedate",width=100)
        self.hospital_table.column("expdate",width=100)
        self.hospital_table.column("dailydose",width=100)
        self.hospital_table.column("spo2",width=100)
        self.hospital_table.column("sex",width=100)
        self.hospital_table.column("bp",width=100)
        self.hospital_table.column("age",width=100)
        self.hospital_table.column("medication",width=100)
        self.hospital_table.column("pid",width=100)
        self.hospital_table.column("wt",width=100)
        self.hospital_table.column("pname",width=100)
        self.hospital_table.column("dob",width=100)
        self.hospital_table.column("address",width=100)

        self.hospital_table.pack(fill=BOTH,expand=1)

        self.hospital_table.bind("<ButtonRelease-1>",self.get_cursor)
        self.fetch_data()
    


    #==================================Functionality Declaration==============================
    def iPrescriptiondata(self):
        if (self.Nameoftablets.get()==""or self.ref.get()==""):
            messagebox.showerror("Error","All fields are required")
        else:
            conn=mysql.connector.connect(host="localhost",username="root",password="sqlshriyawork1!",database="hospital")
            my_cursor=conn.cursor()
            my_cursor.execute("insert into hospital values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(
                                                                                                                    self.ref.get(),
                                                                                                                    self.Nameoftablets.get(),
                                                                                                                    self.Dose.get(),
                                                                                                                    self.NumberofTablets.get(),
                                                                                                                    self.Dr.get(),
                                                                                                                    self.issuedate.get(),
                                                                                                                    self.expdate.get(),
                                                                                                                    self.Dailydose.get(),
                                                                                                                    self.spo2.get(),
                                                                                                                    self.sex.get(),
                                                                                                                    self.bp.get(),
                                                                                                                    self.age.get(),
                                                                                                                    self.Medication.get(),
                                                                                                                    self.patientid.get(),
                                                                                                                    self.Weight.get(),
                                                                                                                    self.PatientName.get(),
                                                                                                                    self.dob.get(),
                                                                                                                    self.patientaddress.get()
                                                                                                                    
                                                                                                                    ))
            conn.commit()
            self.fetch_data()
            conn.close()     
            messagebox.showinfo("Success","Record has been inserted")    

    def update_data(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="sqlshriyawork1!",database="hospital")
        my_cursor=conn.cursor()
        my_cursor.execute("update hospital set Name_of_tablet=%s,dose=%s,No_of_tablets=%s,Dr_name=%s,issuedate=%s,expirydate=%s,dailydose=%s,spo2=%s,sex=%s,blood_pressure=%s,age=%s,medication=%s,Reference_No=%s,weight=%s,Patient_name=%s,dob=%s,patient_address=%s where patient_id=%s",(
                                                                                                                                                                                                                                                        
                                                                                                                                                                                                                                                        self.Nameoftablets.get(),
                                                                                                                                                                                                                                                        self.Dose.get(),
                                                                                                                                                                                                                                                        self.NumberofTablets.get(),
                                                                                                                                                                                                                                                        self.Dr.get(),
                                                                                                                                                                                                                                                        self.issuedate.get(),
                                                                                                                                                                                                                                                        self.expdate.get(),
                                                                                                                                                                                                                                                        self.Dailydose.get(),
                                                                                                                                                                                                                                                        self.spo2.get(),
                                                                                                                                                                                                                                                        self.sex.get(),
                                                                                                                                                                                                                                                        self.bp.get(),
                                                                                                                                                                                                                                                        self.age.get(),
                                                                                                                                                                                                                                                        self.Medication.get(),
                                                                                                                                                                                                                                                        self.ref.get(),
                                                                                                                                                                                                                                                        self.Weight.get(),
                                                                                                                                                                                                                                                        self.PatientName.get(),
                                                                                                                                                                                                                                                        self.dob.get(),
                                                                                                                                                                                                                                                        self.patientaddress.get(),
                                                                                                                                                                                                                                                        self.patientid.get()
                                                                                                                                                                                                                                                        ))
        conn.commit()
        conn.close()
        self.fetch_data()
        messagebox.showinfo("Updated","Record has been updated Successfully")

    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="sqlshriyawork1!",database="hospital")
        my_cursor=conn.cursor()
        my_cursor.execute("select * from hospital")
        rows=my_cursor.fetchall()
        if len(rows)!=0:
            self.hospital_table.delete(*self.hospital_table.get_children())
            for i in rows:
                self.hospital_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    def get_cursor(self,event=""):
        cursor_row=self.hospital_table.focus()
        content=self.hospital_table.item(cursor_row)
        row=content["values"]
        self.ref.set(row[0])
        self.Nameoftablets.set(row[1])
        self.Dose.set(row[2])
        self.NumberofTablets.set(row[3])
        self.Dr.set(row[4])
        self.issuedate.set(row[5])
        self.expdate.set(row[6])
        self.Dailydose.set(row[7])
        self.spo2.set(row[8])
        self.sex.set(row[9])
        self.bp.set(row[10])
        self.age.set(row[11])
        self.Medication.set(row[12])
        self.patientid.set(row[13])
        self.Weight.set(row[14])
        self.PatientName.set(row[15])
        self.dob.set(row[16])
        self.patientaddress.set(row[17])

    def iPrescription(self):
        self.txtPrescription.insert(END,"Reference No.:\t\t\t"+self.ref.get()+"\n")
        self.txtPrescription.insert(END,"Name of tablets:\t\t\t"+self.Nameoftablets.get()+"\n")
        self.txtPrescription.insert(END,"Dose:\t\t\t"+self.Dose.get()+"\n")
        self.txtPrescription.insert(END,"No. of tablets:\t\t\t"+self.NumberofTablets.get()+"\n")
        self.txtPrescription.insert(END,"Prescribed by Dr:\t\t\t"+self.Dr.get()+"\n")
        self.txtPrescription.insert(END,"Daily dose:\t\t\t"+self.Dailydose.get()+"\n")
        self.txtPrescription.insert(END,"Sex:\t\t\t"+self.sex.get()+"\n")
        self.txtPrescription.insert(END,"Age:\t\t\t"+self.age.get()+"\n")
        self.txtPrescription.insert(END,"Medication:\t\t\t"+self.Medication.get()+"\n")
        self.txtPrescription.insert(END,"Patient Id:\t\t\t"+self.patientid.get()+"\n")
        self.txtPrescription.insert(END,"Patient Name:\t\t\t"+self.PatientName.get()+"\n")
        self.txtPrescription.insert(END,"Date of Birth:\t\t\t"+self.dob.get()+"\n")
        

    def idelete(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="sqlshriyawork1!",database="hospital")
        my_cursor=conn.cursor()
        query="delete from hospital where patient_id=%s"
        value=(self.patientid.get(),)
        my_cursor.execute(query,value)
        conn.commit()
        conn.close()
        self.fetch_data()
        messagebox.showinfo("Deleted","Record has been deleted Successfully")
    

    def clear(self):
        self.txtref.delete(0,'end')
        self.comNametablet.delete(0,'end')
        self.txtDose.delete(0,'end')
        self.txtNoOfTablets.delete(0,'end')
        self.txtDr.delete(0,'end')
        self.txtIssueDate.delete(0,'end')
        self.txtExpDate.delete(0,'end')
        self.txtDailyDose.delete(0,'end')
        self.txtspo2.delete(0,'end')
        self.txtsex.delete(0,'end')
        self.txtBloodPressure.delete(0,'end')
        self.txtage.delete(0,'end')
        self.txtMedicine.delete(0,'end')
        self.txtPatientId.delete(0,'end')
        self.txtweight.delete(0,'end')
        self.txtPatientName.delete(0,'end')
        self.txtDateOfBirth.delete(0,'end')
        self.txtPatientAddress.delete(0,'end')
        self.txtPrescription.delete("1.0",END)

    def iexit(self):
        iexit=messagebox.askyesno("Hospital Management System","Confirm you want to exit")
        if iexit>0:

            root.destroy()
            return





if __name__ == '__main__':
    main()
    root=Tk()
    ob=Hospital(root)



















