import pandas as pd
import mysql.connector as sql

#Global Variable for Login/Signup
login=False
admin=False


#Initialising MySQL
try:
    conn=sql.connect(host='localhost',user='root',passwd='bestCSproject12@')

    if conn.is_connected():
        print("Connection OK")
    else:
        print("Not OK")

    x=conn.cursor()
    x.execute("create database if not exists jamal;")
    x.execute("use jamal;")
           
except Exception as e:
    print(e)

"""
=================================================================
The functions used for the program are defined below this coloumn
=================================================================
"""
#Function for printing heading 
def headpr():
    print("=="*30,end="\n")
    print(r"""
             _____           __  __                  _   
            | ____|         |  \/  |   __ _   _ __  | |_ 
            |  _|    _____  | |\/| |  / _` | | '__| | __|
            | |___  |_____| | |  | | | (_| | | |    | |_ 
            |_____|         |_|  |_|  \__,_| |_|     \__|
        """)
    print("=="*30,end="\n")

#Function for adding items to our database
def addit():
    x.execute("create table if not exists products(ItemNo int not null primary key,ItemName varchar(30),Category varchar(20),Quantity int,Price decimal(7,2));")
    l=int(input("Enter the item ID added: "))
    m=input("Enter your product name: ")
    t=float(input("Enter item price: "))
    k=input("Enter the category of the item: ")
    c=int(input("Enter the quantity left: "))
    tup=(l,m,k,c,t)
    x.execute("insert into products values(%s,%s,%s,%s,%s)",tup)
    print("Your item has been added successfully...")
    conn.commit()

#Function for removing items from our database
def remit():
    x.execute("create table if not exists products(ItemNo int not null primary key,ItemName varchar(30),Category varchar(20),Quantity int,Price decimal(7,2));")
    l=int(input("Enter the item ID added: "))
    x.execute("delete from products where ItemNo=%s",(l,))
    print("Your item has been added successfully...")
    conn.commit()

#Function for entering sql shell
def fs():
    m=input("Enter your sql query: ")
    x.execute(m)
#Function defined for checking users
def userchk():
    x.execute("create table if not exists users(Username varchar(20) not null primary key,Password varchar(20));")    
    l=input("Please enter your username: ")
    p=input("Please enter your password: ")
    x.execute("select * from users;")
    n=x.fetchall()
    for i in range(len(n)):
        if n[i][0]==l and n[i][1]==p:
            global login
            login = True
            print("Logged in successfully...")
            break
        else:
            print("Kindly check your username and password...")        
            break

#Function for adding users
def useradd():
    global login
    x.execute("create table if not exists users(Username varchar(20) not null primary key,Password varchar(20));")    
    l=input("Please enter your username: ")
    p=input("Please enter your password: ")
    tup=(l,p)
    x.execute("insert into users values(%s,%s)",tup)
    print("Operation completed successfully")
    login=True
    print("Logged in successfully as well")
    conn.commit()

#Function for adding to cart
def cart():
    l=int(input("Enter the product ID you would add: "))
    x.execute("create table if not exists cart(ItemNo int not null primary key,ItemName varchar(30),Category varchar(20),Price decimal(7,2));")
    x.execute("insert into cart select * from products where ItemNo=%s",(l,))
    
#Function for clearing cart 
def clrcart():
    x.execute("drop table cart;")

#Function for searching by category
def catsearch():
    m=input("Enter the category name with which you want to search: ")
    x.execute("select * from products where Category=%s ",(m,))
    print(x.fetchone())

#Function for proceeding to checkout
def checkout():
    x.execute("select * from cart;")
    print(x.fetchall())
    x.execute("select SUM(Price) from cart;")
    print("The total price of all the combined items: ", x.fetchall(),sep="")
    y=str(input("These are the items in your cart would you like to checkout (Y/N): "))
    if y=='Y':
        
        print("You have purchased the items successfully.....")

def show():
    x.execute("create table if not exists products(ItemNo int not null primary key,ItemName varchar(30),Category varchar(20),Quantity int,Price decimal(7,2));")
    query="select * from products;"
    result_dataFrame = pd.read_sql(query,conn)
    print("=="*30)
    print(result_dataFrame)
    

"""
=======================================
The menu while loop is defined as below
=======================================
"""


#Login check 
while True:
    haha=int(input("Would you like to login/signup\n1.Login\n2.Signup\n3.Enter in ADMIN mode\nEnter the number of the operation you would like to do: "))
    if haha==1:
        userchk()
        break
    if haha==2:
        useradd()
        break
    if haha==3:
        admin=True
        break
    else:
        continue


#Login verification and portal to program        
if login==True:
    while True:
        headpr()
        hello=int(input("""Welcome to the E-Mart Ecommerce platform
                        What would you like to do:
                        1.See the list of products
                        2.Search products based on category
                        3.Add to cart
                        4.Clear cart
                        5.Proceed to checkout                        
                        """))
        if hello==1:
            show()
        if hello==2:
            catsearch()
        if hello==3:
            cart()    
        if hello==4:
            clrcart()
        if hello==5:
            checkout()
        
        
if admin==True:
    while True:
        headpr()
        
        hello=int(input("""Welcome to the E-Mart Ecommerce platform
                        What would you like to do:
                        1.Add items
                        2.Remove items
                        3.Enter SQL Shell                        
                        """))
        if hello==1:
            for i in range(10):    
                addit()
        if hello==2:
            remit()
        if hello==3:
            fs()
else:
    print("The user has not been signed in....\nPlease re-run the program")
