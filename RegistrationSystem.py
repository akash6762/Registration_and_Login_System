
"""   AKASH V   akashvelu1@gmail.com    DW24   TASK-1   """

""" This is registration and login system with mysql database it gets the 
email id, user name, password as user input and stores it in the mysql database.
The mail id and paasword is validated using regular expression . Email id and
password is inserted in the database only if it is validated. After the 
credentials are inserted into the database we are good to go with the login
part. You can login using your (username or email) and password if you forgot 
the passsword you can retrive the password using forgot password option.
"""


import mysql.connector
import re

# mysql server
con = mysql.connector.connect(host = "localhost", 
                              user = "root", 
                              password = "Password@12", 
                              database = "user_credentials")
mycursor = con.cursor()

def validate_password(password_value):
    
    if len(password_value) < 6:
        print("Your password is lesser than 6 characters")
    elif re.search(r"[!@#$%&]", password_value) is None:
        print("Your password must contain one special character")
    elif re.search(r"[0-9]", password_value) is None:
        print("Your password must contain one number")
    elif re.search(r"[a-z]", password_value) is None:
        print("Your password must contain one lower case letter")
    elif re.search(r"[A-Z]", password_value) is None:
        print("Your password must contain one upper case letter")
    elif len(password_value) > 18:
        print("Your password is greater than 18 characters")
    else:
        return True

def validate_email(email_id):
    
    pattern = r'\b[a-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.search(pattern, email_id):
        return True

def register():

    # getting input from the user 
    
    # getting user name
    user_name = str(input("Enter the user name : "))
    
    # getting email id
    while True:
        email = str(input("enter you email id : "))
        if validate_email(email):
            break
        
    # getting password    
    while True:
        password = str(input("Set you password : "))
        if validate_password(password):
            break
    
    # sqk query to insert the user input the sql server
    sql_query = "insert into user_credentials.user_details(user_name, email, password) VALUES(%s, %s, %s)"
    values  = (user_name, email, password)
    mycursor.execute(sql_query, values)
    con.commit()
    
    if mycursor.execute:
        print("Registered successfully")

def login():

    NameOrEmail = str(input("Enter your email id or user name : "))
    password = str(input("Enter your password : "))
    
    sql_query = f"select * from user_credentials.user_details where (user_name = '{NameOrEmail}' or email = '{NameOrEmail}') and password = '{password}'"                                       
    mycursor.execute(sql_query)
    result = mycursor.fetchall()
    
    
    if result == []:
        print("Oops Error occurred Invalid user name or password")
        recover_choice = int(input("Forgot password ? press 1 to recover password : "))
        
        # this if condition is writen to recover the password if the user forgot the password 
        # it takes the user name and email as the input and if the user name and
        # email id is already registered and has an account then it gives the password 
        if recover_choice == 1:
            print("Enter your email id and user name to recover password")
            
            recover_username = str(input("Enter the user name : "))
            recover_email = str(input("Enter email id : "))
            
            # this if condition gets the name and email as the user input
            # and checks if the email and user name is already registered if the 
            # user gives the correct user name and email the variable result 
            # contains the user information in a tuple inside a list and it 
            # prints the password using index values if the user enters 
            # wrong credentials it raises a value error
            
            sql_query = f"select * from user_credentials.user_details where email= '{recover_email}' or user_name = '{recover_username}'"
            mycursor.execute(sql_query)
            result = mycursor.fetchall()
            print(f"Your password is {result[0][2]}")
        else: 
            raise ValueError("Invalid User name or Password")
    else:
        
        # the variable (result) gives the the row containing the details of the 
        # user if the user only if the user gives the correct 
        # (email or username) and password if this condition meets the user 
        # must have created an account already.
        print("YAAY You've logged in")


if __name__ == "__main__":
     
    choice = int(input("Enter 1 for Registration and 2 for Log in : "))
    if choice == 1:
        register()
    elif choice == 2:
        login()
