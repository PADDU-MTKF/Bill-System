import barcode
from tkinter import *
import threading
from barcode.writer import ImageWriter
import mysql.connector as mysql
import random as r  
import os

file=None
#******************************************************************************
mydb=mysql.connect(host='localhost',user='root',passwd='333555333') # connecting with the MySQL
cursor=mydb.cursor()

try: 
    cursor.execute('use item_list')  

except:
    cursor.execute('create database item_list')  
    cursor.execute('use item_list')  
    cursor.execute('create table items(code varchar(40) primary key not null,name varchar(50) not null,price varchar(10) not null,stock varchar(50) not null,MRP varchar(10) not null)')

location =os.getcwd()
                    
try:
    os.chdir(location+'\\barcode')
except:
    os.mkdir(location+'\\barcode')
    os.chdir(location+'\\barcode')

#******************************************************************************

def home(Event=None): # home page of program

    last.pack_forget()
    cont.pack_forget()
    b1.pack(pady=10)
    b2.pack(pady=10)
    b3.pack(pady=10)
    b4.pack(pady=10)


def main_code(code,barname=None):
    def next_part(Event):
        def next_part2(Event):
            def next_part3(Event):
                def next_part4(Event):
                    
                    stock=eeee.get()
                    pstock.pack_forget()
                    eeee.pack_forget()

                    try:
                        if len(name)<1 or len(name)>10:
                            temp=10/0  # rais error and go to exception
                        temp=float(rate)
                        temp=float(stock)
                        temp=float(mrp)
                        command= '\''+code+'\',\''+name+'\',\''+rate+'\',\''+stock+'\',\''+mrp+'\''
                        global file
                        if barname!=None:
                            Bar=file.save(barname)

                    except:
                        command=''

                    
                    
                    global last
                    try:
                        cursor.execute('insert into items value ('+command+')')
                        last=Label(main,text='***** PRODUCT SAVED *****',fg='lightgreen',bg='gray')
                    except:
                        
                        last=Label(main,text='***** ERROR *****',fg='red',bg='gray')       
                        
                    mydb.commit() # saving all changes made to the database 
                    cont.focus()
                    
                    last.pack(pady=5)
                    cont.pack(pady=5)


                rate=eee.get()
                prate.pack_forget()
                eee.pack_forget()

                pstock=Label(main,text='***** STOCK:Packet/Kg *****',bg='skyblue')
                pstock.pack(pady=5)
                eeee=Entry(main)
                eeee.focus()
                eeee.bind('<Return>',next_part4)
                eeee.pack(pady=5)


            mrp=ee.get()
            mrprate.pack_forget()
            ee.pack_forget()
            
            prate=Label(main,text='***** RATE Per Packet/Kg *****',bg='skyblue')
            prate.pack(pady=5)
            eee=Entry(main)
            eee.focus()
            eee.bind('<Return>',next_part3)
            eee.pack(pady=5)

            
            
        name=e.get()
        pname.pack_forget()
        e.pack_forget()
        
        mrprate=Label(main,text='***** MRP PER Packet/Kg *****',bg='skyblue')
        mrprate.pack(pady=5)
        ee=Entry(main)
        ee.focus()
        ee.bind('<Return>',next_part2)
        ee.pack(pady=5)
       
    
    pname=Label(main,text='***** PRODUCT NAME *****',bg='skyblue')
    pname.pack(pady=5)
    e=Entry(main)
    e.focus()
    e.bind('<Return>',next_part)
    e.pack(pady=5)
    



def all_code(): # get all used code for uniqe code 
    list_code=[]         
    cursor.execute('select code from items')     
    for i in cursor:                               
        for j in i:                    
            list_code.append(j)           
    
    return list_code     


def scan_bar():
    def next_part(Event):
        code=e1.get()
        txt.pack_forget()
        e1.pack_forget()
        main_code(code)
        
    b1.pack_forget()
    b2.pack_forget()
    b3.pack_forget()
    b4.pack_forget()
    txt=Label(main,text='***** SCAN THE BARCODE *****',bg='skyblue')
    e1=Entry(main)
    e1.focus()
    e1.bind('<Return>',next_part)
    txt.pack(pady=5)
    e1.pack(pady=5)
    
def gen_bar():
    def save(Event):
        #Bar=file.save(e1.get())
        file_name.pack_forget()
        e1.pack_forget()
        main_code(code,e1.get())
        
    init=barcode.get_barcode_class('code128')  
    b1.pack_forget()
    b2.pack_forget()
    b3.pack_forget()
    b4.pack_forget()
    e1=Entry(main)
    e1.bind('<Return>',save)
    e1.focus()
    file_name=Label(text='***** GIVE NAME FOR THE BARCODE ***** ',bg='skyblue')
    file_name.pack(pady=5)
    e1.pack(pady=5)
    

    list_code=all_code()     #------------------- getting list of all account number in the data base
    
    while True:
        code=str(r.randint(1000000000,1000000000000))    # generating acc no. using random module
        if code in list_code:             #--------------------> if the generated accno is in the data base 
            continue                          #--------------------> then generating another accno untill it is unique
        else:
            break   
    data=code
    global file
    file=init(data,writer=ImageWriter())
    
def updata(): #updating product
    def next_part(Event):
        def change(do):
            upb1.pack_forget()
            upb2.pack_forget()
            upb3.pack_forget()
            upb4.pack_forget()
            en=Entry(main)
            en.focus()
            def up1(Event):
                text.pack_forget()
                en.pack_forget()
                dat=en.get()
                
                global last
                try:
                    cursor.execute('update items set '+do+'='+'\''+dat+'\''+' where code='+'\''+code+'\'')
                    if do=='name':
                        last=Label(main,text='***** NAME CHANGED *****',fg='lightgreen',bg='gray')
            
                    elif do=='stock':
                        last=Label(main,text='***** STOCK CHANGED *****',fg='lightgreen',bg='gray')
                except:
                    
                    last=Label(main,text='***** ERROR *****',fg='red',bg='gray')
                
                mydb.commit() # saving all changes made to the database 
                tit.pack_forget()
                cont.focus()
                
                last.pack(pady=5)
                cont.pack(pady=5)
                    
                
            
            if do=='name':
                text=Label(main,text='***** GIVE NEW NAME *****',bg='skyblue')
                en.bind('<Return>',up1)
                text.pack(pady=5)
                en.pack(pady=5)
            elif do=='price':
                def change__(a,f=None):
                    def up2(Event):
                        text.pack_forget()
                        dat=en.get()
                        en.pack_forget()
                        
                        global last
                        try:
                            cursor.execute('update items set '+a+'='+'\''+dat+'\''+' where code='+'\''+code+'\'')
                            if a=='price':
                                last=Label(main,text='***** RATE CHANGED *****',fg='lightgreen',bg='gray')
                                
                            elif a=='mrp':
                                last=Label(main,text='***** MRP CHANGED *****',fg='lightgreen',bg='gray')
                                
                            
                        except:
                           
                            last=Label(main,text='***** ERROR *****',fg='red',bg='gray')
                        
                        mydb.commit() # saving all changes made to the database 
                        
                        if f != None:
                            
                            if f==0:
                                tit.pack_forget()
                                cont.focus()
                                last=Label(main,text='***** MRP & RATE CHANGED *****',fg='lightgreen',bg='gray')
                                last.pack(pady=5)
                                cont.pack(pady=5)
                            else:
                                change__('price',0)

                        else:
                            tit.pack_forget()
                            cont.focus()
                            
                            last.pack(pady=5)
                            cont.pack(pady=5)
                            
                    try:
                        rb.pack_forget()
                        mb.pack_forget()
                        rmb.pack_forget()
                    except:
                        pass

                    en=Entry(main)
                    en.focus()
                    
                    if a=='price':
                        text=Label(main,text='***** GIVE NEW RATE *****',bg='skyblue')
                        en.bind('<Return>',up2)
                        text.pack(pady=5)
                        en.focus()
                        en.pack(pady=5)
                    elif a=='mrp':
                        text=Label(main,text='***** GIVE NEW MRP *****',bg='skyblue')
                        en.bind('<Return>',up2)
                        text.pack(pady=5)
                        en.focus()
                        en.pack(pady=5)
                    elif a=='rm':
                        
                        change__('mrp',1)
                        



                rb=Button(main,text='Change Product RATE',fg='blue',bg='lightgreen',command=lambda:change__('price'))
                mb=Button(main,text='Change Product MRP',fg='blue',bg='lightgreen',command=lambda:change__('mrp'))
                rmb=Button(main,text='Change Product RATE & MRP',fg='blue',bg='lightgreen',command=lambda:change__('rm'))

                rb.pack(pady=5)
                mb.pack(pady=5)
                rmb.pack(pady=5)

                
           
            elif do=='stock':
                text=Label(main,text='***** GIVE NEW STOCK *****',bg='skyblue')
                en.bind('<Return>',up1)
                text.pack(pady=5)
                en.pack(pady=5)

            elif do=='delete':
                global last
                cursor.execute('delete from items where code='+'\''+code+'\'')
                last=Label(main,text='***** PRODUCT DELETED *****',fg='lightgreen',bg='gray')
                mydb.commit() # saving all changes made to the database 
                tit.pack_forget()
                cont.focus()
                
                last.pack(pady=5)
                cont.pack(pady=5)    
         
            
        code=e1.get()
        txt.pack_forget()
        e1.pack_forget()
        cursor.execute('select * from items where code=\''+code+'\'')
        global last
        for i in cursor:                               
            data=list(i)
            tit=Label(main,text=data[1]+' :-MRP = RS. '+data[4]+' || Rate = RS. '+data[2]+' per packet/kg \n( '+data[3]+' packet/kg in stock )',fg='white',bg='gray')
            tit.pack(pady=5)
            upb1=Button(main,text='Change Product Name',fg='blue',bg='lightgreen',command=lambda:change('name'))
            upb2=Button(main,text='Change RATE OR MRP',fg='blue',bg='lightgreen',command=lambda:change('price'))
            upb3=Button(main,text='EDIT STOCK',fg='blue',bg='lightgreen',command=lambda:change('stock'))
            upb4=Button(main,text='DELETE Product',fg='red',bg='lightgreen',command=lambda:change('delete'))
            upb1.pack(pady=5)
            upb2.pack(pady=5)
            upb3.pack(pady=5)
            upb4.pack(pady=5)
            break
        else:
            last=Label(main,text='***** NO PRODUCT WITH THIS CODE *****',fg='red',bg='gray')
            cont.focus()      
            last.pack(pady=5)
            cont.pack(pady=5)
            
    
    b1.pack_forget()
    b2.pack_forget()
    b3.pack_forget()
    b4.pack_forget()

    txt=Label(main,text='***** SCAN THE BARCODE *****',bg='skyblue')
    e1=Entry(main)
    e1.focus()
    e1.bind('<Return>',next_part)
    txt.pack(pady=5)
    e1.pack(pady=5)

def view():
    def next_part(Event):
        def subhome(Event=None):
            pcode.pack_forget()
            pname.pack_forget()
            mrate.pack_forget()
            prate.pack_forget()
            pstock.pack_forget()
            home()

        code=e1.get()
        txt.pack_forget()
        e1.pack_forget()
        cursor.execute('select * from items where code=\''+code+'\'')
        global last
        for i in cursor:                               
            data=list(i)
            pcode=Label(main,text='Product Code  :- '+data[0],bg='skyblue')
            pname=Label(main,text='Product Name  :- '+data[1],bg='skyblue')
            prate=Label(main,text='Product Rate  :- '+data[2],bg='skyblue')
            mrate=Label(main,text='Product MRP   :- '+data[4],bg='skyblue')
            pstock=Label(main,text='Product Stock :- '+data[3],bg='skyblue')
            
            pcode.pack(pady=5)
            pname.pack(pady=5)
            mrate.pack(pady=5)
            prate.pack(pady=5)
            pstock.pack(pady=5)
            global cont
            cont=Button(main,text='CLICK here To Continue',fg='blue',bg='lightgreen',command=subhome)
            cont.focus()
            cont.bind('<Return>',subhome)
            cont.pack(pady=5)
            break
        else:
            last=Label(main,text='***** NO PRODUCT WITH THIS CODE *****',fg='red',bg='gray')
            cont.focus()      
            last.pack(pady=5)
            cont.pack(pady=5)

    b1.pack_forget()
    b2.pack_forget()
    b3.pack_forget()
    b4.pack_forget()

    txt=Label(main,text='***** SCAN THE BARCODE *****',bg='skyblue')
    e1=Entry(main)
    e1.focus()
    e1.bind('<Return>',next_part)
    txt.pack(pady=5)
    e1.pack(pady=5)



#GUI*********************************************************************

main=Tk()   #creating main window
main.geometry('400x250+500+50')    #set size of window
main.configure(bg='gray')
main.resizable(height=False,width=False)
main.title('ADD ITEM')        #title of window


lab=Label(main,text='  ADD ITEM TO DATABASE  ',fg='yellow',bg='gray')
und=Label(main,text='`-`'*35,fg='gold',bg='gray')
lab.pack(pady=5)
und.pack()

b1=Button(main,text='1) BAR CODE + ADD DATA ',fg='blue',bg='lightgreen',command=gen_bar)
b2=Button(main,text='2)'+' '*(10)+'ADD DATA '+' '*(13),fg='blue',bg='lightgreen',command=scan_bar)
b3=Button(main,text='3)'+' '*(6)+'UPDATE DATA '+' '*(10),bg='lightgreen',fg='blue',command=updata)
b4=Button(main,text='4) VIEW PRODUCT DETAILS',bg='lightgreen',fg='blue',command=view)

last=Label(main,text='***** PRODUCT SAVED *****')
cont=Button(main,text='CLICK here To Continue',fg='blue',bg='lightgreen',command=home)
cont.bind('<Return>',home)

th=threading.Thread(target=home)
th.daemon=True
th.start()

main.mainloop()
sys.exit()