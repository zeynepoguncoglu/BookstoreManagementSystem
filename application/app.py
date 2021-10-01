import mysql.connector as sql
from tkinter import *
import random
from tkinter import messagebox
from tkinter import ttk
import datetime

situation=2

def login_gui():
    win = Tk()
    win.geometry("450x450")
    win.title("Login Page")

    customervl = Label(win, text="Customer ID :")

    global customerid1
    customerid1 = Entry(win, textvariable=StringVar())

    customerid1.place(x=200, y=150)

    customervl.place(x=50, y=150)

    enter = Button(win, text="Enter", command=lambda: login(), bd=0)
    enter.configure(bg="pink")

    signin = Button(win, text="Sign In", command=lambda: new_customer_gui(), bd=0)
    enter.configure(bg="pink")

    enter.place(x=240, y=200)
    signin.place(x=280, y=200)

    win.mainloop()

def login():
    global db
    db = sql.connect(host="127.0.0.1", user="root", passwd="***", database="bookstore")
    cur = db.cursor()

    global customerid
    customerid = customerid1.get()

    while True:
        customerid = customerid1.get()
        cur.execute("select * from customer where customer_id = (%s)" % (customerid))
        rud = cur.fetchall()
        if rud:
            welcome = 'Welcome ' + customerid + '!'
            messagebox.showinfo("Welcome", welcome)
            display_order_gui()
            break
        else:
            warning = 'There is no registered Customer ID ' + customerid + '. Please sign in.'
            messagebox.showinfo("Warning", warning)
            new_customer_gui()

        if (db.is_connected()):
           db.close()
           print("MySQL connection is closed.")

        cur.close()
        db.close()

def new_customer_gui():
    win = Tk()
    win.geometry("500x500")
    win.title("Sign In Page")

    namelvl = Label(win, text="Customer Name :")
    surnamelvl = Label(win, text="Customer Surname :")
    emaillvl = Label(win, text="Customer Email :")
    citycodelvl = Label(win, text="Customer City Code :")
    citylvl = Label(win, text="Customer City :")

    global name1
    name1 = Entry(win, textvariable=StringVar())
    global surname1
    surname1 = Entry(win, textvariable=StringVar())
    global email1
    email1 = Entry(win, textvariable=StringVar())
    global citycode1
    citycode1 = Entry(win, textvariable=IntVar())
    global city1
    city1 = Entry(win, textvariable=StringVar())

    name1.place(x=200, y=150)
    surname1.place(x=200, y=200)
    email1.place(x=200, y=250)
    citycode1.place(x=200, y=300)
    city1.place(x=200, y=350)

    namelvl.place(x=50, y=150)
    surnamelvl.place(x=50, y=200)
    emaillvl.place(x=50, y=250)
    citycodelvl.place(x=50, y=300)
    citylvl.place(x=50, y=350)

    enter = Button(win, text="Enter", command=lambda: new_customer(), bd=0)
    enter.configure(bg="pink")

    enter.place(x=238, y=400)

    win.mainloop()

def new_customer ():

    db = sql.connect(host="127.0.0.1", user="root", passwd="***", database="bookstore")
    cur = db.cursor()

    name = name1.get()
    surname = surname1.get()
    email = email1.get()
    citycode = citycode1.get()
    city = city1.get()

    recordcitytuple = (citycode,city,)
    customer_id = random.randrange(100000,1000000)
    recordcustomertuple = (customer_id,name, surname, email, citycode)

    while True:
        citycode = citycode1.get()
        cur.execute("select * from city where customer_city_code = (%s)" % (citycode))
        rud = cur.fetchall()
        if rud:
            warning = citycode +' - ' + city + ' exists.'
            messagebox.showinfo("Warning", warning)
            break
        else:
            insert_statement = """insert into city values (%s, %s)"""
            try:
                cur.execute(insert_statement, recordcitytuple)
                db.commit()
                print("1 record inserted, ID:", cur.lastrowid)
            except sql.Error as error:
                print("Failed to Insert record to table: {}".format(error))
                db.rollback()

    insert_statement = """insert into customer values (%s, %s, %s, %s, %s)"""

    try:
        cur.execute(insert_statement, recordcustomertuple)
        db.commit()
        print("1 record inserted, ID:", cur.lastrowid)
        success = "Welcome " + name + ' ' + surname + '! ' + '\nYour Customer ID is ' + str(customer_id) +'.'\
                  + '\nPlease note your Customer ID.'
        messagebox.showinfo("Welcome", success)
        messagebox.showinfo("Exit", "Please close the windows and log in again with your Customer ID.")
        quit()
    except sql.Error as error:
        print("Failed to Insert record to table: {}".format(error))
        db.rollback()
    finally:
        if (db.is_connected()):
            db.close()
            print("MySQL connection is closed.")

    cur.close()
    db.close()

def display_order_gui():

    win = Tk()
    win.geometry("450x450")
    win.title("Order Information Page")

    db = sql.connect(host="127.0.0.1", user="root", passwd="***", database="bookstore")
    cur = db.cursor()

    display_statement= ("SELECT order_book.order_id, orders.order_date, book.book_name "
                        "FROM (((orders "
                        "INNER JOIN customer ON orders.customer_id = customer.customer_id) "
                        "INNER JOIN order_book ON orders.order_id = order_book.order_id) "
                        "INNER JOIN book ON order_book.isbn = book.isbn) "
                        "where customer.customer_id =(%s)") % (customerid)

    cur.execute(display_statement)
    data = cur.fetchall()
    alldata = ''
    for record in data:
        alldata += str(record[0]) + '\t' + '\t' + str(record[1]) + '\t' + str(record[2]) + "\n"

    orderlabel1 = Label(win, text='Find your order(s) below:')
    orderlabel2 = Label(win, text='Order ID \t\t Order Date \t Book Name')
    orderlabel3 = Label(win, text=alldata)
    orderlabel1.place(x=10, y=10)
    orderlabel2.place(x=10, y=30)
    orderlabel3.place(x=10, y=50)

    neworder = Button(win, text="New Order", command=lambda: preparation())
    neworder.place(x=250, y=100)

    exit = Button(win, text="Exit", command=lambda: quit())
    exit.place(x=330, y=100)

    win.mainloop()

def preparation():
    messagebox.showinfo("","Please close the windows to continue.")
    global situation
    situation = 5

def new_order():
    db = sql.connect(host="127.0.0.1", user="root", passwd="***", database="bookstore")
    cur = db.cursor()

    current_stock_statement = """select book_stock from book"""
    cur.execute(current_stock_statement)
    data = cur.fetchall()

    set_statement = """update book set book_stock = (%s) where isbn = (%s)"""

    orders()
    global isbn

    if (var1.get() == 1):
        if data[0][0]>=1:
            tup = ((data[0][0] - 1), 100000001)
            isbn = 100000001
            cur.execute(set_statement, tup)
            db.commit()
            order_book()
        else:
            messagebox.showinfo("Sorry","Sorry, there is no enough stock for ISBN:100000001.")

    if (var2.get() == 1):
        if data[1][0] >= 1:
            tup = ((data[1][0] - 1), 100000002)
            isbn = 100000002
            cur.execute(set_statement, tup)
            db.commit()
            order_book()
        else:
            messagebox.showinfo("Sorry", "Sorry, there is no enough stock for ISBN:100000002.")

    if (var3.get() == 1):
        if data[2][0]>=1:
            tup = ((data[2][0] - 1), 100000003)
            isbn = 100000003
            cur.execute(set_statement, tup)
            db.commit()
            order_book()
        else:
            messagebox.showinfo("Sorry","Sorry, there is no enough stock for ISBN:100000003.")

    if (var4.get() == 1):
        if data[3][0] >= 1:
            tup = ((data[3][0] - 1), 100000004)
            isbn = 100000004
            cur.execute(set_statement, tup)
            db.commit()
            order_book()
        else:
            messagebox.showinfo("Sorry", "Sorry, there is no enough stock for ISBN:100000004.")

    if (var5.get() == 1):
        if data[4][0] >= 1:
            tup = ((data[4][0] - 1), 100000005)
            isbn = 100000005
            cur.execute(set_statement, tup)
            db.commit()
            order_book()
        else:
            messagebox.showinfo("Sorry", "Sorry, there is no enough stock for ISBN:100000005.")

    if (var6.get() == 1):
        if data[5][0] >= 1:
            tup = ((data[5][0] - 1), 100000006)
            isbn = 100000006
            cur.execute(set_statement, tup)
            db.commit()
            order_book()
        else:
            messagebox.showinfo("Sorry", "Sorry, there is no enough stock for ISBN:100000006.")

    if (var7.get() == 1):
        if data[6][0] >= 1:
            tup = ((data[6][0] - 1), 100000007)
            isbn = 100000007
            cur.execute(set_statement, tup)
            db.commit()
            order_book()
        else:
            messagebox.showinfo("Sorry", "Sorry, there is no enough stock for ISBN:100000007.")

    if (var8.get() == 1):
        if data[7][0] >= 1:
            tup = ((data[7][0] - 1), 100000008)
            isbn = 100000008
            cur.execute(set_statement, tup)
            db.commit()
            order_book()
        else:
            messagebox.showinfo("Sorry", "Sorry, there is no enough stock for ISBN:100000008.")

    if (var9.get() == 1):
        if data[8][0] >= 1:
            tup = ((data[8][0] - 1), 100000009)
            isbn = 100000009
            cur.execute(set_statement, tup)
            db.commit()
            order_book()
        else:
            messagebox.showinfo("Sorry", "Sorry, there is no enough stock for ISBN:100000009.")

def orders():
    db = sql.connect(host="127.0.0.1", user="root", passwd="***", database="bookstore")
    cur = db.cursor()
    order_first_part = 'ABC'
    order_second_part = str(random.randrange(10007,100000))
    global order
    order = order_first_part+order_second_part

    date = datetime.datetime.today()
    date_correct = str(date.year) + '-' + str(date.month) + '-' + str(date.day)

    insert_statement = """insert into orders values (%s,%s,%s)"""

    var = (order, str(date_correct), customerid)

    cur.execute(insert_statement, var)
    db.commit()

def order_book():
    db = sql.connect(host="127.0.0.1", user="root", passwd="***", database="bookstore")
    cur = db.cursor()
    var = (order,isbn,1)
    insert_statement = """insert into order_book values (%s,%s,%s)"""
    cur.execute(insert_statement, var)
    print(var)
    db.commit()

def new_order_gui():
    root = Tk()
    root.title("New Order Page")
    global var1
    global var2
    global var3
    global var4
    global var5
    global var6
    global var7
    global var8
    global var9

    var1 = IntVar()
    check1 = Checkbutton(root, text="100000001 - 16:50 Train", variable=var1)
    check1.pack()

    var2 = IntVar()
    check2 = Checkbutton(root, text="100000002 - Ah Mana Mu", variable=var2)
    check2.pack()

    var3 = IntVar()
    check3 = Checkbutton(root, text="100000003 - Flowers", variable=var3)
    check3.pack()

    var4 = IntVar()
    check4 = Checkbutton(root, text="100000004 - Hiç Yoktan İyidir", variable=var4)
    check4.pack()

    var5 = IntVar()
    check5 = Checkbutton(root, text="100000005 - Unbelievable", variable=var5)
    check5.pack()

    var6 = IntVar()
    check6 = Checkbutton(root, text="100000006 - Hiç Yoktan İyidir", variable=var6)
    check6.pack()

    var7 = IntVar()
    check7 = Checkbutton(root, text="100000007 - Agatha’nın Anahtarı", variable=var7)
    check7.pack()

    var8 = IntVar()
    check8 = Checkbutton(root, text="100000008 - Marriage", variable=var8)
    check8.pack()

    var9 = IntVar()
    check9 = Checkbutton(root, text="100000009 - Flowers", variable=var9)
    check9.pack()

    b = Button(root, text="Give Order", command=lambda :new_order())
    b.pack()

    exit = Button(root, text="Exit", command=lambda: quit())
    exit.pack()

    root.geometry("400x400+120+120")
    root.mainloop()


def quit():
    messagebox.showinfo("Exit", "MySQL connection is closed.")
    messagebox.showinfo("Exit", "Please close the windows.")
    db.close()
    print("MySQL connection is closed.")


login_gui()

if situation == 5:
    new_order_gui()
else:
    pass