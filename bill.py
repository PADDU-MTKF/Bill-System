from tkinter import *
import threading
import mysql.connector as mysql
from tkinter import ttk
from datetime import datetime
import os

path=os.getcwd()
#******************************************************************************
mydb=mysql.connect(host='localhost',user='root',passwd='root') # connecting with the MySQL
cursor=mydb.cursor()

try: 
    cursor.execute('use item_list')  
    try:
        cursor.execute('create table billno(billno int(10) primary key not null)')
        cursor.execute('insert into billno values(0)')
        mydb.commit()
    except:
    	pass

except:
    print('ADD Some data First')
    os.sys.exit()

location =os.getcwd()
					
try:
	os.chdir(location+'\\bill')
except:
	os.mkdir(location+'\\bill')
	os.chdir(location+'\\bill')

#******************************************************************************

Total=0.00
data=[]
pnt=0
stock=[]

def home():
	global total
	global e1
	global dele
	global new
	
	total=Label(main,text='\n\nScan Code'+' '*60+'TOTAL :- '+str(Total),bg='lightgray',font='Verdana 11 bold italic')
	total.pack(side=RIGHT,padx=20)
    
	e1.focus()
	e1.bind('<Return>',get_info)
	e1.pack(padx=32,side='left')
	dele.pack(side=RIGHT,padx=20)
	new.pack(side=RIGHT,padx=20)


def all_code(): # get all used code for uniqe code 
    list_code=[]         
    cursor.execute('select code from items')     
    for i in cursor:                               
        for j in i:                    
            list_code.append(j)           
    
    return list_code    

def new():
	global Total,data,pnt,stock
	Total=0.00
	data=[]
	pnt=0
	stock=[]
	a=tree.get_children()
	if a!= '()':
		for child in a:
			tree.delete(child)

	total.pack_forget()
	e1.pack_forget() or e2.pack_forget()
	dele.pack_forget()
	new.pack_forget()
	home()

def delete_item():
	
	try:
		ind=list(tree.selection())
		p=(tree.item(ind)['values'][0])
		global data
		global stock
		global Total
		global total

		data.pop(int(p)-1)
		stock.pop(int(p)-1)

		a=tree.get_children()
		if a!= '()':
			for child in a:
				tree.delete(child)
		
		
		total.pack_forget()
		e1.pack_forget() or e2.pack_forget()
		dele.pack_forget()
		new.pack_forget()
		
		Total=0.00
		for i in data:
			no=str(data.index(i)+1)
			text=[]
			text.append(no)
			for j in i:
				text.append(j)
			
			Total+=float(i[2])
			tree.insert('',END,value=text)
		home()
		

	except:
		pass
	e1.focus() or e2.focus()

def get_info(Event):
	global total
	global e2
	global pnt
	global Total
	
	e1.pack_forget()
	total.pack_forget()
	dele.pack_forget()
	new.pack_forget()

	def qty(Event):
		
		total.pack_forget()
		qty=e2.get()
		try:
			ttemp=float(qty)
		except:
			qty=''
		if qty == ''or qty=='0':
			qty='1'

		e2.pack_forget()
		dele.pack_forget()
		new.pack_forget()
		
		cursor.execute('select * from items where code=\''+code+'\'')
		global Total
		global data
		global stock


		
		a=tree.get_children()
		if a!= '()':
			for child in a:
				tree.delete(child)

		
		for i in cursor:
			product=[i[1],qty,str(float(qty)*float(i[2])),i[2],i[4]]
			st=[code,qty]
		
		

		for i in data:
			if product[0]==i[0]:
				ind=data.index(i)
				try:
					data[ind][1]=str(int(data[ind][1])+int(product[1]))
				except:
					data[ind][1]=str(float(data[ind][1])+float(product[1]))

				data[ind][2]=str(float(data[ind][2])+float(product[2]))
				stock[ind][1]=data[ind][1]

				break
		else:
			data.append(product)
			stock.append(st)
		Total=0.00
		
		for i in data:
			no=str(data.index(i)+1)
			text=[]
			text.append(no)
			for j in i:
				text.append(j)
			
			Total+=float(i[2])
			tree.insert('',END,value=text)
			
			
			
		e2.delete(first=0,last=END)
		home()
	code=e1.get()
	e1.delete(first=0,last=END)
	if code!='':
		pnt=0
		list_code=all_code()
		if code in list_code:
			total=Label(main,text='\n\nQUANTITY '+' '*60+'TOTAL :- '+str(Total),bg='lightgray',font='Verdana 11 bold italic')
			total.pack()
			e2.focus()
			e2.bind('<Return>',qty)
			e2.pack(padx=32,side='left')
			dele.pack(side=RIGHT,padx=20)
			new.pack(side=RIGHT,padx=20)

		else:
			home()
	else:
		pnt+=1
		if pnt==2 and data!=[]:
			payment=Toplevel(main)
			payment.geometry('400x200+600+250')
			payment.configure(bg='lightgray')
			payment.resizable(height=False,width=False)
			payment.title('PAYMENT')  
			
			ttl=Label(payment,text=' '*15+'TOTAL :- ',bg='lightgray',font='Verdana 15 bold italic')
			tmont=Label(payment,text=str(Total),bg='lightgray',font='Verdana 15 bold italic')
			amo=Entry(payment)
			amolab=Label(payment,text='Amount Received :- ',bg='lightgray',font='Verdana 15 italic')
			
			def final_step(Event):
				global Total
				
				rec=amo.get()
				try:
					balance=float(rec)-float(Total)
				except:
					amo.delete(first=0,last=END)
					rec=Total
					amo.insert(END,rec)

					balance=float(rec)-float(Total)

				bal=Label(payment,text=' '*11+'BALANCE :- ',bg='lightgray',fg='green',font='Verdana 15 italic')
				balamo=Label(payment,text=str(balance),bg='lightgray',fg='green',font='Verdana 15 bold italic')


				

				def print_rcpt(Event=None):
					
					payment.destroy()
					global Total,data,pnt,stock

					for i in stock:
						code=i[0]
						cursor.execute('select stock from items where code=\''+code+'\'')
						for j in cursor:
							for q in j:
								
								try:

									new_stock=str(float(q)-float(i[1]))
								except:
									print('hi')
									new_stock=str(0)
								cursor.execute('update items set stock='+'\''+new_stock+'\''+' where code=\''+code+'\'')
								mydb.commit() # saving all changes made to the database 

					cursor.execute('update billno set billno=billno+1')
					mydb.commit() # saving all changes made to the database 
					cursor.execute('select * from billno')
					for i in cursor:
						for j in i:
							billno=j
							
					
					#*************************************************************************
					
					filename=str(billno)+'.txt'
					file=open(filename,'w')
					d=datetime.now()
					date=d.strftime('%B %d %Y')
					time=d.strftime('%H:%M:%S')
					Total='%.2f'%Total
					
        			

					billtext='''
                      BILL                         
___________________________________________________
              My GENERAL STORES                             
     My Residency, 5'th Block, Wakanda                     
   
Contact No. : +911234567890
              +910987654321
___________________________________________________
Bill No. :- '''+str(billno)+'''                                       
Date     :- '''+str(date)+'''
Time     :- '''+str(time)+'''
                           
Item           Qty.      MRP      Rate      Amount   
___________________________________________________\n'''      
					file.write(billtext)


					for i in data:
						Bitem=str(i[0])
						Bqty='%.2f'%float(i[1])
						Bmrp='%.2f'%float(i[4])
						Brate='%.2f'%float(i[3])
						Bamount='%.2f'%float(i[2])

						billtext=Bitem+' '*(12-len(Bitem))+' '*(6-len(str(Bqty)))+Bqty+'  '+' '*(8-len(str(Bmrp)))+Bmrp+'  '+' '*(8-len(str(Brate)))+Brate+'  '+' '*(10-len(str(Bamount)))+Bamount
						file.write('\n'+billtext)


					billtext='''
___________________________________________________

Items : '''+str(len(data))+' '*(19-len(str(len(data))))+'''Total(Rs.):- '''+' '*(10-len(str(Total)))+Total+'''
___________________________________________________


          ********** THANK YOU **********           
					'''
					file.write(billtext)
					file.close()



					#**************************************************************************
					
					os.startfile(filename,'print')   # print recipt
					

					Total=0.00
					data=[]
					pnt=0
					stock=[]
					a=tree.get_children()
					if a!= '()':
						for child in a:
							tree.delete(child)

					total.pack_forget()
					e1.pack_forget() or e2.pack_forget()
					dele.pack_forget()
					new.pack_forget()
					home()

				canc=Button(payment,text='PRINT',fg='green',command=print_rcpt)
				

				bal.grid(column=1,row=2,pady=10)
				balamo.grid(column=2,row=2)
				canc.grid(column=2,row=3,pady=10)
				canc.bind('<Return>',print_rcpt)
				canc.focus()

				

			ttl.grid(column=1,row=0,pady=10)
			tmont.grid(column=2,row=0)
			amo.grid(column=2,row=1)
			amolab.grid(column=1,row=1,padx=10)
			amo.bind('<Return>',final_step)
			amo.focus()
			pnt=0
		
		home()

#GUI*********************************************************************

main=Tk()   #creating main window
height=main.winfo_screenheight()
width=main.winfo_screenwidth()
main.geometry('%dx%d+0+0'% (width,height))    #set size of window
main.configure(bg='lightgray')
main.resizable(height=False,width=False)
main.title('BILLING')        #title of window




rm_img=PhotoImage(file=path+'\\resource\\remove.png').subsample(4,4)
new_img=PhotoImage(file=path+'\\resource\\new.png').subsample(3,4)

title=Label(main,text='LAKSHMI GENERAL STORE',bg='lightgray',font='Verdana 30 bold italic')
und=Label(main,text='`~`~'*32,bg='lightgray',font='Verdana 5 bold italic')
phone=Label(main,text='\nGSTIN :- 152515344584535'+' '*100+'Phone :- 9845697582',bg='lightgray',font='Verdana 15 bold italic')
dele=Button(main,image=rm_img,bg='lightgray',activebackground='lightgray',command=delete_item,borderwidth=0)
new=Button(main,image=new_img,bg='lightgray',activebackground='lightgray',command=new,borderwidth=0)

tree=ttk.Treeview(main,columns=(1,2,3,4),show='headings',height=19)


total=Label(main)
title.pack()
und.pack()
phone.pack()

e1=Entry(main)
e2=Entry(main)

tree.column(1,width=3,anchor='center')
#tree.column(2,anchor='center')
tree.column(3,width=5,anchor='center')
tree.column(4,width=7,anchor='center')

tree.pack(side=TOP,fill=BOTH,padx=25,pady=5)
tree.heading(1,text='S.No.')
tree.heading(2,text='Product Name')
tree.heading(3,text='Quantity')
tree.heading(4,text='Price')



th=threading.Thread(target=home)
th.daemon=True
th.start()

main.mainloop()
os.sys.exit()
