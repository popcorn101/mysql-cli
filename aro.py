import pandas as pd
import mysql.connector as sql

#Global Variable for Login/Signup
login=False
admin=False


#Initialising MySQL
try:
    conn=sql.connect(host='localhost',user='root',passwd='123456')

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
    global login  # Declare global to modify it
    x.execute(
        "CREATE TABLE IF NOT EXISTS users(Username VARCHAR(20) NOT NULL PRIMARY KEY, Password VARCHAR(20));"
    )
    l = input("Please enter your username: ").strip()
    p = input("Please enter your password: ").strip()
    
    # Directly check for user in the database
    x.execute("SELECT * FROM users WHERE Username = %s AND Password = %s", (l, p))
    user = x.fetchone()  # Fetch only one record
    
    if user:
        login = True
        print("Logged in successfully...")
    else:
        print("Invalid username or password. Please try again.")


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
    l = int(input("Enter the product ID you would like to add to the cart: "))

    # Ensure `cart` table exists
    x.execute("""
        CREATE TABLE IF NOT EXISTS cart(
            ItemNo INT NOT NULL PRIMARY KEY,
            ItemName VARCHAR(30),
            Category VARCHAR(20),
            Price DECIMAL(7,2)
        );
    """)

    # Check if the product exists and has sufficient quantity
    x.execute("SELECT ItemName, Category, Price, Quantity FROM products WHERE ItemNo = %s", (l,))
    product = x.fetchone()

    if product:
        item_name, category, price, quantity = product
        
        if quantity > 0:
            # Insert the item into the `cart` table
            x.execute(
                "INSERT INTO cart (ItemNo, ItemName, Category, Price) VALUES (%s, %s, %s, %s)",
                (l, item_name, category, price)
            )
            # Reduce the quantity by 1 in the `products` table
            x.execute("UPDATE products SET Quantity = Quantity - 1 WHERE ItemNo = %s", (l,))
            conn.commit()  # Commit both changes
            print(f"{item_name} has been added to the cart.")
        else:
            print(f"Sorry, {item_name} is out of stock.")
    else:
        print("The product ID you entered does not exist.")

    
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
