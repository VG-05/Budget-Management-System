import mysql.connector as mysql
import time


con = mysql.connect(host="localhost",user="root",password="tiger")
if con.is_connected():
    print("Connection Successful!")
else:
    print("Connection Unsuccessful. Please try again later")
cur = con.cursor()

#Checking for database Budget
cur.execute("show databases")
databases = cur.fetchall()
for database in databases:
    if database[0].lower() == "budget":                                          #database is a tuple containing one element
        break
#If database Budget not present, create it
else:
    cur.execute("create database Budget")
    con.commit()
#Use the budget database
cur.execute("use Budget")


class Category:
    
    def __init__(self, name):
        #Creating a new budget
        self.name = name
        if self.name not in budgets:
            sql_createtable = "create table {}(amount float, Transaction_type varchar(20))".format(self.name)
            cur.execute(sql_createtable)
            con.commit()
    

    def __str__(self):
        #Displaying Budget on screen
        sql_display = "select * from {}".format(self.name)
        cur.execute(sql_display)
        rows = cur.fetchall()
        title = f"{self.name:*^30}\n"
        items = ''
        total = 0
        for i in range(len(rows)):
            items += f"{rows[i][1][0:23]:23}{rows[i][0]:>7.2f}\n"
            total += rows[i][0]
        output = title + items + "Total: " + str(total)
        return output
    
  
    def check_funds(self, amount):
        sql_display = "select * from {}".format(self.name)
        cur.execute(sql_display)
        rows = cur.fetchall()
        total_amount = 0
        for row in rows:
          total_amount += row[0]
        if amount <= total_amount:
            return True
        else:
            return False
        
        
    def deposit(self, amount, des = 'deposit'):
        sql_insert = "insert into {} values({}, '{}')".format(self.name, amount, des)
        cur.execute(sql_insert)
        con.commit()


    def withdraw(self, amount, des = 'withdrawal'):
        if self.check_funds(amount):
            sql_insert = "insert into {} values({}, '{}')".format(self.name, amount, des)
            cur.execute(sql_insert)
            con.commit()
            return True
        else:
            return False

    def get_balance(self):
        sql_display = "select * from {}".format(self.name)
        cur.execute(sql_display)
        rows = cur.fetchall()
        total_amount = 0
        for row in rows:
          total_amount += row[0]
        return total_amount
  
  
    def transfer(self, amount, categoryto):
        if self.check_funds(amount):
            self.withdraw(-amount, "Transfer to " + categoryto.name)
            categoryto.deposit(amount, "Transfer from " + self.name)
            return True
        else:
            return False
    
    def delete(self):
        sql_delete = "drop table {}".format(self.name)
        cur.execute(sql_delete)
        con.commit()
    

while True:
    print('''                         MENU
    ________________________________________________________
    1. Create a new budget category
    2. Display all Budget category names
    3. Display a Budget category
    4. Deposit Funds into a Budget category
    5. Withdraw Funds from a Budget category 
    6. Transfer funds from one Budget catergory to another 
    7. Display balance of a Budget category
    8. Delete budget
    9. Save & Exit
    ''')
    choice = int(input("Enter choice: "))
    
    
    budgets = list()                                         #creating a budgets list containing the name of all budgets. Placed here because budgets var used in defining Category
    sql_showtables = "show tables"
    cur.execute(sql_showtables)
    tables = cur.fetchall()
    for table in tables:
        budgets.append(table[0])               #table is a tuple containing one element
    
    
    if choice == 1:
        budget = Category(input("Enter budget name: "))
        print("Budget Created!")
        time.sleep(1)
        
        
    elif choice == 2:
        print(budgets)
        time.sleep(2)
        
        
    elif choice == 3:
        budget = Category(input("Enter budget category to display: "))
        print(budget)
        time.sleep(5)
        
        
    elif choice == 4:
        budget = Category(input("Enter budget name to deposit funds to: "))
        dep = float(input("Enter amount of funds to deposit: "))
        depdesc = input("Enter description of deposit: ")
        if depdesc:
            budget.deposit(dep, depdesc)
        else:
            budget.deposit(dep)
        print("Deposit Successful!")
        time.sleep(1)
        
        
    elif choice == 5:
        budget = Category(input("Enter budget name to withdraw funds from: "))
        wd = float(input("Enter amount of funds to withdraw: "))
        wddesc = input("Enter description of withdrawal: ")
        if wddesc:
            budget.withdraw(-wd, wddesc)
        else:
            budget.withdraw(-wd)
        print("Withdrawal Successful!")
        time.sleep(1)
        
        
    elif choice == 6:
        budget1 = Category(input("Enter budget name to withdraw funds from: "))
        budget2 = Category(input("Enter budget name to deposit funds to: "))
        dep = float(input("Enter amount of funds to deposit: "))
        budget1.transfer(dep, budget2)
        print("Transfer Successful")
        time.sleep(1)
    
    
    elif choice == 7:
        budget = Category(input("Enter budget name to get balance from: "))
        try:
            print(budget.get_balance())
        except:
            print(budget.name,"does not exist")
        time.sleep(2)
    
    
    elif choice == 8:
        budget = Category(input("Enter budget name to delete: "))
        budget.delete()
        print("Deletion Successful!")
        time.sleep(1)
        
        
    elif choice == 9:
        break
    
    
    else:
        print("Please enter a number  1-9")
        time.sleep(1)
        continue
