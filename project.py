from tkinter import *
from PIL import ImageTk, Image
import sqlite3
from tkinter.ttk import Combobox
from abc import abstractmethod
import tkinter.ttk as ttk

# username = 'Ayezan'
# password= 'Ayezanse201003'

window = Tk()
# FOR LOGIN SCREEN
LOGINTEXT = StringVar()
USERNAME = StringVar()
PASSWORD = StringVar()
SEARCH = StringVar()

class ActionHandler:
    login_count = 0
    @staticmethod
    def login_button_command():
        DataBaseHandler.create_user()
        is_success = DataBaseHandler.query_user()
        if (is_success):
            View.option_view(window)
        else:
            if ActionHandler.login_count == 3:
                window.destroy()
            else:
                ActionHandler.login_count = ActionHandler.login_count + 1
                LOGINTEXT.set("Note: Incorrect Username or Password, Please try again...")
    @staticmethod
    def medicine_button_command():
        View.medicine_window()
    @staticmethod
    def patient_button_command():
        View.add_patient_window()
    @staticmethod
    def doctor_button_command():
        View.doctor_window()
    @staticmethod
    def exit_button_command():
        exit()
    @staticmethod
    def show_medicine_button_command():
        View.ShowView()
    @staticmethod
    def save_doctor_button_command():
        #using abstract class here
        if(DOCTOR_DOCTOR_TYPE.get() =="Cardiologist"):
            doctor = Cardiologist(DOCTOR_NAME.get(),DOCTOR_AGE.get(), DOCTOR_GENDER.get(), DOCTOR_PHONENUM.get(), DOCTOR_CNIC.get())
        else:
            doctor = Surgeon(DOCTOR_NAME.get(),DOCTOR_AGE.get(), DOCTOR_GENDER.get(), DOCTOR_PHONENUM.get(), DOCTOR_CNIC.get())

        doctor.add_doctor()
        window_doctor.destroy()
    @staticmethod
    def save_medicine_button_command():
        medicine = Medicines()
        # USING OVERLOADING FUNCTIONALITY HERE
        if(MEDICINE_COMPANY.get() == "" or MEDICINE_NAME.get()=="" or MEDICINE_TYPE.get()==""):
            status = medicine.add_medicine(amount=MEDICINE_AMOUNT.get(),price=MEDICINE_PRICE.get())
        elif(MEDICINE_AMOUNT.get()==""):
            status = medicine.add_medicine(company = MEDICINE_COMPANY.get(),type =MEDICINE_TYPE.get(),name=MEDICINE_NAME.get(),price=MEDICINE_PRICE.get())
        elif(MEDICINE_PRICE.get()==""):
            status = medicine.add_medicine(company = MEDICINE_COMPANY.get(),type =MEDICINE_TYPE.get(),name=MEDICINE_NAME.get(),amount=MEDICINE_AMOUNT.get())
        else:
            status = medicine.add_medicine(MEDICINE_COMPANY.get(),MEDICINE_NAME.get(),MEDICINE_TYPE.get(),MEDICINE_AMOUNT.get(),MEDICINE_PRICE.get())
        if(status == True):
            window_medicine.destroy()
    @staticmethod
    def save_patient_button_command():
        patient = Patients(PATIENT_NAME.get(),PATIENT_GENDER.get(),PATIENT_AGE.get(),PATIENT_PHONENUM.get(),PATIENT_DOC_CONSULT.get(),PATIENT_CNIC.get())
        toDestroy = patient.add_patients()
        if toDestroy:
            window_patient.destroy()
class DataBaseHandler:
    global con, cursor
    @staticmethod
    def create_user():
        global  con, cursor
        con = sqlite3.connect("Pharmacy.db")
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS 'USERS' (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
        cursor.execute("SELECT * FROM 'USERS' ORDER BY 'id' DESC LIMIT 1")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO 'USERS' ('username','password') VALUES('Ayezan','Ayezanse201003')")
        con.commit()
    @staticmethod
    def insert_into_doctor(name, age, gender, phoneNum, CNIC,doctorType):
        con = sqlite3.connect("Pharmacy.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO 'DOCTORS' ('name','age','gender','phoneNum','CNIC','doctorType') VALUES(?,?,?,?,?,?)",(name, age, gender, phoneNum, CNIC,doctorType))
        con.commit()
    @staticmethod
    def DisplayData():
        DataBaseHandler.create_user()
        cursor.execute("SELECT * FROM 'MEDICINES'")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        con.close()

    @staticmethod
    def query_user():
        con = sqlite3.connect("Pharmacy.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM USERS WHERE username = ? AND password = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is None:
            return False
        else:
            return True
    @staticmethod
    def create_all_tables():
        con=sqlite3.connect("Pharmacy.db")
        cursor=con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS 'MEDICINES'(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT,type TEXT,amount TEXT,price TEXT,company TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS 'PATIENTS'(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT,gender TEXT,age TEXT,phoneNum TEXT,doctorConsulted TEXT,cnic TEXT)")
        cursor.execute("CREATE TABLE IF NOT EXISTS 'DOCTORS'(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT,age TEXT,gender TEXT,phoneNum TEXT,CNIC TEXT,doctorType TEXT)")
        con.commit()
    @staticmethod
    def insert_into_medicine(company,name,type,amount,price):
        con=sqlite3.connect("Pharmacy.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO 'MEDICINES' ('company','name','type','amount','price') VALUES(?,?,?,?,?)",(company,name,type,amount,price))
        con.commit()
    @staticmethod
    def insert_into_patient(name,gender,age,phoneNum,doctorConsulted,CNIC):
        con = sqlite3.connect("Pharmacy.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO 'PATIENTS' ('name','gender','age','phoneNum','doctorConsulted','CNIC') VALUES(?,?,?,?,?,?)",(name,gender,age,phoneNum,doctorConsulted,CNIC))
        con.commit()
    @staticmethod
    def fetch_doc_name():
        con = sqlite3.connect("Pharmacy.db")
        cursor = con.cursor()
        cursor.execute("SELECT name FROM 'DOCTORS'")
        doc_name = cursor.fetchall()
        return doc_name

class Medicines:
    # WE ARE DOING METHOD OVERLOADING
    def add_medicine(self,company=None,name=None,type=None,amount=None,price=None):
        status = True
        if (((company!=None) and (company!="")) & ((name!=None) and (name!="")) & ((type!=None) and (type!="")) & ((amount!=None) and (amount!="")) & ((price!=None) and (price!=""))):
            DataBaseHandler.insert_into_medicine(company, name, type, amount, price)
        elif ((company!=None and company!="") & (name!=None and name!="") & (type!=None and type!="") & (amount!=None and amount!="")):
            DataBaseHandler.insert_into_medicine(company, name, type, amount,str(100))
        elif((company!=None and company!="") & (name!=None and name!="") & (type!=None and type!="") & (price!=None and price!="")):
            DataBaseHandler.insert_into_medicine(company, name, type,str(1),price)
        else:
            MANDATORY_MEDICINE_FIELD.set("Not making entry, Required fields are not provided")
            status = False
        return status
class Doctor:
    def __init__(self,name,age,gender,phoneNum,CNIC):
        self.name=name
        self.age=age
        self.gender=gender
        self.CNIC=CNIC
        self.phoneNum=phoneNum
    @abstractmethod
    def add_doctor(self):
        pass
class Cardiologist(Doctor):
    def __init__(self,name,age,gender,phoneNum,CNIC):
        super().__init__(name,age,gender,phoneNum,CNIC)

    def add_doctor(self):
        if (((self.name!=None) and (self.name!="")) & ((self.age!=None) and (self.age!="")) & ((self.gender!=None) and (self.gender!="")) & ((self.phoneNum!=None) and (self.phoneNum!="")) & ((self.CNIC!=None) and (self.CNIC!=""))):
            DataBaseHandler.insert_into_doctor(self.name,self.age,self.gender,self.phoneNum,self.CNIC,"Cardiologist")
        else:
            MANDATORY_DOCTOR_FIELD.set("Not making entry, Required fields are not provided")
class Surgeon(Doctor):
    def __init__(self, name, age, gender, phoneNum, CNIC):
        super().__init__(name, age, gender, phoneNum, CNIC)

    def add_doctor(self):
        if (((self.name != None) and (self.name != "")) & ((self.age != None) and (self.age != "")) & ((self.gender != None) and (self.gender != "")) & ((self.phoneNum != None) and (self.phoneNum != "")) & ((self.CNIC != None) and (self.CNIC != ""))):
            DataBaseHandler.insert_into_doctor(self.name, self.age, self.gender, self.phoneNum, self.CNIC,"Surgeon")
        else:
            MANDATORY_DOCTOR_FIELD.set("Not making entry, Required fields are not provided")

class Patients:
    def __init__(self,name,gender,age,phoneNum,doctorConsulted,CNIC):
        self.name=name
        self.gender=gender
        self.age=age
        self.phoneNum=phoneNum
        self.doctorConsulted=doctorConsulted
        self.CNIC=CNIC
    def add_patients(self):
        isSuccess=False
        if (((self.name != None) and (self.name != "")) & ((self.gender != None) and (self.gender != "")) & ((self.age != None) and (self.age != "")) & ((self.phoneNum != None) and (self.phoneNum != "")) & ((self.doctorConsulted != None) and (self.doctorConsulted != "")) & ((self.CNIC != None) and (self.CNIC != ""))):
            DataBaseHandler.insert_into_patient(self.name, self.gender, self.age, self.phoneNum, self.doctorConsulted,self.CNIC)
            isSuccess=True
        else:
            MANDATORY_PATIENT_FIELD.set("Not making entry, Required fields are not provided")

        return isSuccess

class View:
    @staticmethod
    def login_View(window):
        View.set_window(window)
        Label(window, text="\nInventory Management of Bin Hashim Pharmacy", font=("Basic Retro", 35),bg='Sky Blue').pack()
        MainFrame = Frame(window).pack()
        HeadFrame = Frame(MainFrame).pack()
        image = Image.open("pic1.png").convert("RGB")
        Label(HeadFrame, text="\nLogin Screen\n", font=("Basic Retro", 20), bg='Sky Blue').pack()
        image = image.resize((200,200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        lbl = Label(HeadFrame, image=img,bg="Sky Blue")
        lbl.image = img
        lbl.pack()
        Label(HeadFrame, text="\nUsername", font=("Basic Retro", 16), bg='Sky Blue').pack()
        Entry(HeadFrame, bd=3, textvariable=USERNAME).pack()
        Label(HeadFrame, text="\nPassword", font=("Basic Retro", 16), bg='Sky Blue').pack()
        Entry(HeadFrame, bd=3, show="*", textvariable=PASSWORD).pack()
        Label(HeadFrame, text="\n", bg='Sky Blue').pack()
        Button(HeadFrame, text="Login", command=ActionHandler.login_button_command, fg='White', bg='Black',font=("Bold"), width=13).pack()
        Label(HeadFrame, textvariable=LOGINTEXT, font=("Basic Retro", 10), bg='Sky Blue', fg='Red').pack()
    @staticmethod
    def option_view(window):
        window.destroy()
        window = Tk()
        Label(window, text="\nInventory Management of Bin Hashim Pharmacy", font=("Basic Retro", 35),bg='Sky Blue').pack()
        View.set_window(window)
        Label(window, text="\n", bg='Sky Blue').pack()
        Button(window,text='Add Medicine',command=ActionHandler.medicine_button_command,bd=3,fg='white',bg='Black',font=("Bold"),width=20,height=2).pack()
        Label(window,text="\n",bg='Sky Blue').pack()
        Button(window,text='Add Patient',command=ActionHandler.patient_button_command,bd=3,fg='white',bg='Black',font=("Bold"),width=20,height=2).pack()
        Label(window,text="\n",bg='Sky Blue').pack()
        Button(window,text='Doctor',command=ActionHandler.doctor_button_command,bd=3,fg='white',bg='Black',font=("Bold"),width=20,height=2).pack()
        Label(window,text="\n",bg='Sky Blue').pack()
        Button(window,text='Exit',command=ActionHandler.exit_button_command,bd=3,fg='white',bg='Black',font=("Bold"),width=20,height=2).pack()
        window.mainloop()
    @staticmethod
    def set_window(setup):
        setup.title("Inventory Management of Bin Hashim Pharmacy")
        width = setup.winfo_screenwidth()
        height = setup.winfo_screenheight()
        setup.geometry(f'{width}x{height}')
        setup.config(bg='Sky Blue')
    @staticmethod
    def ShowView():
        global tree
        global viewform
        viewform = Toplevel()
        Label(viewform, text="\nShow Medicine", font=("Basic Retro", 35), bg='Sky Blue').pack()
        View.set_window(viewform)
        Label(viewform, text="\n", bg='Sky Blue').pack()
        tree = ttk.Treeview(viewform, columns=("ProductID", "Product Name", "Product Type", "Product Amount", "Product Price", "Company Name"),selectmode="extended",height=25)
        tree.heading('ProductID', text="ProductID", anchor=W)
        tree.heading('Product Name', text="Product Name", anchor=W)
        tree.heading('Product Type', text="Product Type", anchor=W)
        tree.heading('Product Amount', text="Product Amount", anchor=W)
        tree.heading('Product Price', text="Product Price", anchor=W)
        tree.heading('Company Name', text="Company Name", anchor=W)
        tree.column('#0', stretch=NO, minwidth=0, width=120)
        tree.column('#1', stretch=NO, minwidth=0, width=120)
        tree.column('#2', stretch=NO, minwidth=0, width=120)
        tree.column('#3', stretch=NO, minwidth=0, width=120)
        tree.column('#4', stretch=NO, minwidth=0, width=120)
        tree.column('#5', stretch=NO, minwidth=0, width=120)
        tree.pack()
        DataBaseHandler.DisplayData()
    @staticmethod
    def medicine_window():
        global window_medicine
        window_medicine = Toplevel()
        global MEDICINE_NAME
        global MEDICINE_TYPE
        global MEDICINE_AMOUNT
        global MEDICINE_COMPANY
        global MEDICINE_PRICE
        global MANDATORY_MEDICINE_FIELD
        # FOR MEDICINE SCREEN
        MEDICINE_NAME = StringVar()
        MEDICINE_TYPE = StringVar()
        MEDICINE_AMOUNT = StringVar()
        MEDICINE_PRICE = StringVar()
        MEDICINE_COMPANY = StringVar()
        MANDATORY_MEDICINE_FIELD = StringVar()
        Label(window_medicine, text="Medicine Detail",font=("Basic Retro",35),bg='Sky Blue').pack()
        View.set_window(window_medicine)
        Label(window_medicine,text="\nName",font=("Basic Retro", 16),bg='Sky Blue').pack()
        Entry(window_medicine,bd=3,textvariable=MEDICINE_NAME).pack()
        Label(window_medicine, text="\nType",font=("Basic Retro", 16),bg='Sky Blue').pack()
        combo=Combobox(window_medicine,textvariable=MEDICINE_TYPE)
        combo['values']=('Choose..','Liquid','Tablet','Capsule','Drops','Injection')
        combo.current(0)
        combo.pack()
        Label(window_medicine, text="\nQuantity",font=("Basic Retro", 16),bg='Sky Blue').pack()
        Entry(window_medicine, bd=3,textvariable=MEDICINE_AMOUNT).pack()
        Label(window_medicine, text="\nPrice",font=("Basic Retro", 16),bg='Sky Blue').pack()
        Entry(window_medicine, bd=3,textvariable=MEDICINE_PRICE).pack()
        Label(window_medicine, text="\nCompany",font=("Basic Retro", 16),bg='Sky Blue').pack()
        combo = Combobox(window_medicine,textvariable=MEDICINE_COMPANY)
        combo['values'] = ('Choose..','ABC Company','XYZ Company','Premium Medicare','Noble Pharmaceuticals')
        combo.current(0)
        combo.pack()
        Label(window_medicine,text="\n", bg='Sky Blue').pack()
        Button(window_medicine,text='Show Medicine',command=ActionHandler.show_medicine_button_command,bd=3,fg='Black',bg='Blue',font=("Bold"),width=20,height=1).pack()
        Label(window_medicine, text="\n", bg='Sky Blue').pack()
        Button(window_medicine,text='Save',command=ActionHandler.save_medicine_button_command,bd=3,fg='Black',bg='Blue',font=("Bold"),width=20,height=1).pack()
        Label(window_medicine, textvariable=MANDATORY_MEDICINE_FIELD, bg='Sky Blue',fg='Red').pack()
        window_medicine.mainloop()
    @staticmethod
    def doctor_window():
        global window_doctor
        window_doctor = Toplevel()
        global DOCTOR_NAME
        global DOCTOR_AGE
        global DOCTOR_GENDER
        global DOCTOR_PHONENUM
        global DOCTOR_CNIC
        global DOCTOR_DOCTOR_TYPE
        global MANDATORY_DOCTOR_FIELD
        # FOR DOCTOR SCREEN
        DOCTOR_NAME = StringVar()
        DOCTOR_AGE = StringVar()
        DOCTOR_GENDER = StringVar()
        DOCTOR_PHONENUM = StringVar()
        DOCTOR_CNIC = StringVar()
        DOCTOR_DOCTOR_TYPE = StringVar()
        MANDATORY_DOCTOR_FIELD = StringVar()
        Label(window_doctor, text="Doctor Detail", font=("Basic Retro", 35), bg='Sky Blue').pack()
        View.set_window(window_doctor)
        Label(window_doctor, text="\nName", font=("Basic Retro", 16), bg='Sky Blue').pack()
        Entry(window_doctor, bd=3, textvariable=DOCTOR_NAME).pack()
        Label(window_doctor, text="\nGender", font=("Basic Retro", 16), bg='Sky Blue').pack()
        combo = Combobox(window_doctor, textvariable=DOCTOR_GENDER)
        combo['values'] = ('Choose..', 'Male', 'Female', 'Other')
        combo.current(0)
        combo.pack()
        Label(window_doctor, text="\nAge", font=("Basic Retro", 16), bg='Sky Blue').pack()
        Entry(window_doctor, bd=3, textvariable=DOCTOR_AGE).pack()
        Label(window_doctor, text="\nPhone Number", font=("Basic Retro", 16), bg='Sky Blue').pack()
        Entry(window_doctor, bd=3, textvariable=DOCTOR_PHONENUM).pack()
        Label(window_doctor, text="\nCNIC", font=("Basic Retro", 16), bg='Sky Blue').pack()
        Entry(window_doctor, bd=3, textvariable=DOCTOR_CNIC).pack()
        Label(window_doctor, text="\nType", font=("Basic Retro", 16), bg='Sky Blue').pack()
        combo = Combobox(window_doctor, textvariable=DOCTOR_DOCTOR_TYPE)
        combo['values'] = ('Choose..', 'Cardiologist', 'Surgeon')
        combo.current(0)
        combo.pack()
        Label(window_doctor, text="\n", font=("Basic Retro", 16), bg='Sky Blue').pack()
        Button(window_doctor, text='Save', command=ActionHandler.save_doctor_button_command, bd=3, fg='Black',bg='Blue', font=("Bold"), width=20, height=1).pack()
        Label(window_doctor, textvariable=MANDATORY_DOCTOR_FIELD, bg='Sky Blue', fg='Red').pack()
        window_doctor.mainloop()
    @staticmethod
    def add_patient_window():
        global window_patient
        window_patient = Toplevel()
        global PATIENT_NAME
        global PATIENT_GENDER
        global PATIENT_AGE
        global PATIENT_PHONENUM
        global PATIENT_DOC_CONSULT
        global PATIENT_CNIC
        global MANDATORY_PATIENT_FIELD
        # FOR DOCTOR SCREEN
        PATIENT_NAME = StringVar()
        PATIENT_GENDER = StringVar()
        PATIENT_AGE = StringVar()
        PATIENT_PHONENUM = StringVar()
        PATIENT_DOC_CONSULT = StringVar()
        PATIENT_CNIC = StringVar()
        MANDATORY_PATIENT_FIELD = StringVar()
        Label(window_patient, text="Add Patient", font=("Basic Retro", 35), bg='Sky Blue').pack()
        View.set_window(window_patient)
        Label(window_patient, text="\nName", font=("Basic Retro", 16), bg='Sky Blue').pack()
        Entry(window_patient, bd=3, textvariable=PATIENT_NAME).pack()
        Label(window_patient, text="\nGender", font=("Basic Retro", 16), bg='Sky Blue').pack()
        combo = Combobox(window_patient, textvariable=PATIENT_GENDER)
        combo['values'] = ('Choose..', 'Male', 'Female', 'Other')
        combo.pack()
        Label(window_patient, text="\nAge", font=("Basic Retro", 16), bg='Sky Blue').pack()
        Entry(window_patient, bd=3, textvariable=PATIENT_AGE).pack()
        Label(window_patient, text="\nPhone Number", font=("Basic Retro", 16), bg='Sky Blue').pack()
        Entry(window_patient, bd=3, textvariable=PATIENT_PHONENUM).pack()
        Label(window_patient, text="\nDoctor Consult", font=("Basic Retro", 16), bg='Sky Blue').pack()
        combo = Combobox(window_patient, textvariable=PATIENT_DOC_CONSULT)
        combo['values'] = (DataBaseHandler.fetch_doc_name())
        combo.pack()
        Label(window_patient, text="\nCNIC", font=("Basic Retro", 16), bg='Sky Blue').pack()
        Entry(window_patient, bd=3, textvariable=PATIENT_CNIC).pack()
        Label(window_patient, text="\n", font=("Basic Retro", 16), bg='Sky Blue').pack()
        Button(window_patient, text='Save', command=ActionHandler.save_patient_button_command, bd=3, fg='Black',
               bg='Blue', font=("Bold"), width=20, height=1).pack()
        Label(window_patient, textvariable=MANDATORY_PATIENT_FIELD, bg='Sky Blue', fg='Red').pack()
        window_patient.mainloop()

if __name__ == '__main__':
    DataBaseHandler.create_all_tables()
    View.login_View(window)
    window.mainloop()