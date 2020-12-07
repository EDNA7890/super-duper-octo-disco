from tkinter import *
from tkinter import ttk
import tkinter.messagebox as tmsg
import os
import time

#===================Python Variables=======================
menu_category = ["Starters","Starters","Main Course","Main Course","Drinks","Drinks","Dessert","Tea&Coffee"]

menu_category_dict = {"Starters":"1 Starters.txt","Main Course":"2 Main Course.txt","Drinks":"4 Drinks.txt","Tea&Coffee":"5 Tea&Beverage.txt"}

order_dict = {}
for i in menu_category:
    order_dict[i] = {}

os.chdir(os.path.dirname(os.path.abspath(__file__)))
#====================Backend Functions===========================
def load_menu():
    menuCategory.set("")
    menu_tabel.delete(*menu_tabel.get_children())
    menu_file_list = os.listdir("Menu")
    for file in menu_file_list:
        f = open("Menu\\" + file , "r")
        category=""
        while True:
            line = f.readline()
            if(line==""):
                menu_tabel.insert('',END,values=["","",""])
                break
            elif (line=="\n"):
                continue
            elif(line[0]=='#'):
                category = line[1:-1]
                name = "\t\t"+line[:-1]
                price = ""
            elif(line[0]=='*'):
                name = line[:-1]
                price = ""
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ")+1:-3]
            
            menu_tabel.insert('',END,values=[name,price,category])
        #menu_tabel.insert('',END,values=["Masala Dosa","50"])

def load_order():
    order_tabel.delete(*order_tabel.get_children())
    for category in order_dict.keys():
        if order_dict[category]:
            for lis in order_dict[category].values():
                order_tabel.insert('',END,values=lis)
    update_total_price()
    
def load_item_from_menu(event):
    cursor_row = menu_tabel.focus()
    contents = menu_tabel.item(cursor_row)
    row = contents["values"]

    itemName.set(row[0])
    itemRate.set(row[1])
    itemCategory.set(row[2])
    itemQuantity.set("1")

def load_item_from_order(event):
    cursor_row = order_tabel.focus()
    contents = order_tabel.item(cursor_row)
    row = contents["values"]

    itemName.set(row[0])
    itemRate.set(row[1])
    itemQuantity.set(row[2])
    itemCategory.set(row[4])

def show_button_operation():
    category = menuCategory.get()
    if category not in menu_category:
        tmsg.showinfo("Error", "Please select valid Choice")
    else:
        menu_tabel.delete(*menu_tabel.get_children())
        f = open("Menu\\" + menu_category_dict[category] , "r")
        while True:
            line = f.readline()
            if(line==""):
                break
            if (line[0]=='#' or line=="\n"):
                continue
            if(line[0]=='*'):
                name = "\t"+line[:-1]
                menu_tabel.insert('',END,values=[name,"",""])
            else:
                name = line[:line.rfind(" ")]
                price = line[line.rfind(" ")+1:-3]
                menu_tabel.insert('',END,values=[name,price,category])

def cancel_button_operation():
    names = []
    for i in menu_category:
        names.extend(list(order_dict[i].keys()))
    if len(names)==0:
        tmsg.showinfo("Error", "Your order list is Empty")
        return
    ans = tmsg.askquestion("Cancel Order", "Are You Sure to Cancel Order?")
    if ans=="no":
        return
    order_tabel.delete(*order_tabel.get_children())
    for i in menu_category:
        order_dict[i] = {}
    clear_button_operation()
    update_total_price()
    
def update_total_price():
    price = 0
    for i in menu_category:
        for j in order_dict[i].keys():
            price += int(order_dict[i][j][3])
    if price == 0:
        totalPrice.set("")
    else:
        totalPrice.set("Rs. "+str(price)+"  /-")
        
def close_window():
    tmsg.showinfo("Thanks", "Thanks for using our service")
    root.destroy()
#[name,rate,quantity,str(int(rate)*int(quantity)),category]
#==================Backend Code Ends===============

#================Frontend Code Start==============
root = Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Welcome to Perth Hotels")
#root.attributes('-fullscreen', True)
#root.resizable(0, 0)

#================Title==============
style_button = ttk.Style()
style_button.configure("TButton",font = ("arial",10,"bold"),
   background="lightgreen")

title_frame = Frame(root, bd=8, bg="white", relief=GROOVE)
title_frame.pack(side=TOP, fill="x")

title_label = Label(title_frame, text="Perth Hotels Cancel Order System", 
                    font=("times new roman", 20, "bold"),bg = "white", fg="black", pady=5)
title_label.pack()

#==============Customer=============
customer_frame = LabelFrame(root,text="Customer Menu",font=("times new roman", 15, "bold"),
                            bd=8, bg="lightblue", relief=GROOVE)
customer_frame.pack(side=TOP, fill="x")

customer_name_label = Label(customer_frame, text="Locally Made Food with extra love &taste", 
                    font=("arial", 15, "bold"),bg = "lightblue", fg="blue")
customer_name_label.grid(row = 0, column = 0)

customerName = StringVar()
customerName.set("")
customer_name_entry = Entry(customer_frame,width=20,font="arial 15",bd=5,
                                textvariable=customerName)
customer_name_entry.grid(row = 0, column=1,padx=50)

customer_contact_label = Label(customer_frame, text="Email Address", 
                    font=("arial", 15, "bold"),bg = "lightblue", fg="blue")
customer_contact_label.grid(row = 0, column = 2)

customerContact = StringVar()
customerContact.set("")
customer_contact_entry = Entry(customer_frame,width=20,font="arial 15",bd=5,
                                textvariable=customerContact)
customer_contact_entry.grid(row = 0, column=3,padx=50)

#===============Menu===============
menu_frame = Frame(root,bd=8, bg="sky blue", relief=GROOVE)
menu_frame.place(x=0,y=125,height=585,width=680)

menu_label = Label(menu_frame, text="Menu", 
                    font=("times new roman", 20, "bold"),bg = "white", fg="black", pady=0)
menu_label.pack(side=TOP,fill="x")

menu_category_frame = Frame(menu_frame,bg="sky blue",pady=10)
menu_category_frame.pack(fill="x")

combo_lable = Label(menu_category_frame,text="Select Type", 
                    font=("arial", 12, "bold"),bg = "yellow", fg="black")
combo_lable.grid(row=0,column=0,padx=10)

menuCategory = StringVar()
combo_menu = ttk.Combobox(menu_category_frame,values=menu_category,
                            textvariable=menuCategory)
combo_menu.grid(row=0,column=1,padx=30)

show_button = ttk.Button(menu_category_frame, text="Show",width=10,
                        command=show_button_operation)
show_button.grid(row=0,column=2,padx=60)

show_all_button = ttk.Button(menu_category_frame, text="Show All",
                        width=10,command=load_menu)
show_all_button.grid(row=0,column=3)

############################# Menu Tabel ##########################################
menu_tabel_frame = Frame(menu_frame)
menu_tabel_frame.pack(fill=BOTH,expand=1)

scrollbar_menu_x = Scrollbar(menu_tabel_frame,orient=HORIZONTAL)
scrollbar_menu_y = Scrollbar(menu_tabel_frame,orient=VERTICAL)

style = ttk.Style()
style.configure("Treeview.Heading",font=("arial",13, "bold"))
style.configure("Treeview",font=("arial",12),rowheight=25)

menu_tabel = ttk.Treeview(menu_tabel_frame,style = "Treeview",
            columns =("name","price","category"),xscrollcommand=scrollbar_menu_x.set,
            yscrollcommand=scrollbar_menu_y.set)

menu_tabel.heading("name",text="Name")
menu_tabel.heading("price",text="Price")
menu_tabel["displaycolumns"]=("name", "price")
menu_tabel["show"] = "headings"
menu_tabel.column("price",width=50,anchor='center')

scrollbar_menu_x.pack(side=BOTTOM,fill=X)
scrollbar_menu_y.pack(side=RIGHT,fill=Y)

scrollbar_menu_x.configure(command=menu_tabel.xview)
scrollbar_menu_y.configure(command=menu_tabel.yview)

menu_tabel.pack(fill=BOTH,expand=1)


#menu_tabel.insert('',END,values=["Masala Dosa","50"])
load_menu()
menu_tabel.bind("<ButtonRelease-1>",load_item_from_menu)

###########################################################################################
#==============Order Frame=====================
order_frame = Frame(root,bd=8, bg="sky blue", relief=GROOVE)
order_frame.place(x=680,y=335,height=370,width=680)

order_title_label = Label(order_frame, text="Your Order", 
                    font=("times new roman", 20, "bold"),bg = "yellow", fg="black")
order_title_label.pack(side=TOP,fill="x")

############################## Order Tabel ###################################
order_tabel_frame = Frame(order_frame)
order_tabel_frame.place(x=0,y=40,height=260,width=680)

scrollbar_order_x = Scrollbar(order_tabel_frame,orient=HORIZONTAL)
scrollbar_order_y = Scrollbar(order_tabel_frame,orient=VERTICAL)

order_tabel = ttk.Treeview(order_tabel_frame,
            columns =("name","rate","quantity","price","category"),xscrollcommand=scrollbar_order_x.set,
            yscrollcommand=scrollbar_order_y.set)

order_tabel.heading("name",text="Name")
order_tabel.heading("rate",text="Rate")
order_tabel.heading("quantity",text="Quantity") 
order_tabel.heading("price",text="Price")
order_tabel["displaycolumns"]=("name", "rate","quantity","price")
order_tabel["show"] = "headings"
order_tabel.column("rate",width=100,anchor='center', stretch=NO)
order_tabel.column("quantity",width=100,anchor='center', stretch=NO)
order_tabel.column("price",width=100,anchor='center', stretch=NO)

order_tabel.bind("<ButtonRelease-1>",load_item_from_order)

scrollbar_order_x.pack(side=BOTTOM,fill=X)
scrollbar_order_y.pack(side=RIGHT,fill=Y)

scrollbar_order_x.configure(command=order_tabel.xview)
scrollbar_order_y.configure(command=order_tabel.yview)

order_tabel.pack(fill=BOTH,expand=1)

# order_tabel.insert('',END,text="HEllo",values=["Masala Dosa","50","2","100"])
###########################################################################################

cancel_order_label = Label(order_frame, text="Cancel Order", 
                    font=("arial", 12, "bold"),bg = "yellow", fg="black")
cancel_order_label.pack(side=LEFT,anchor=SW,padx=20,pady=10)

cancel0rder= StringVar()
cancelOrder.set("")
cancel_order_entry = Entry(order_frame, font="arial 12",textvariable=totalPrice,state=DISABLED, 
                            width=10)
cancel_order_entry.pack(side=LEFT,anchor=SW,padx=0,pady=10)

cancel_button = ttk.Button(order_frame, text="Cancel Order",command=cancel_button_operation)
cancel_button.pack(side=LEFT,anchor=SW,padx=20,pady=10)

root.mainloop()
#====================Frontend code ends=====================