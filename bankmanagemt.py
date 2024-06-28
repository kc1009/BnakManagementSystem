
import sqlite3 as sql
import os 
import sys
import datetime as dt
con=sql.connect("bankDB")
table1="create table if not exists customer(accountno int,name varchar(50),gender varchar(7),emailID varchar(25),phoneno  bigint,acct_ype varchar(20), int,active int,primary key(accountno))"
table2="create table if not exists transaction1(accountno int, t_type varchar(20),t_dateb datetime,amount int)"
cur=con.cursor()
cur.execute(table1)
cur.execute(table2)
def createAccount():
    ano=int(input("enter account number:"))
    name=input("enter account holder name:")
    gender=input("enter account holder gender:")
    email=input("enter account holder email id:")
    phone=int(input("enter phone number:"))
    op1=int(input("enter 1 for saving account and 2 for current account:"))
    atype=""
    if op1==1:
        atype="saving"
    elif op1==2:
        atype="current"
    amount=int(input("enter ammount to deposit:"))
    qry="insert into customer values(%d,'%s','%s','%s',%d,'%s',%d,%d)"%(ano,name,gender,email,phone,atype,amount,1)
    cur.execute(qry)
    if cur.rowcount>0:
        print("account created !!!!")
    else:
        print("error in creating the account")
    con.commit()
def viewallaccount():
    qry="select*from customer"
    cur.execute(qry)
    print("-"*80)
    print("%6s %15s %7s %15s %10s %7s %9s "%("accno","name","gender","email","phone","atype","ammount"))
          
    for i in cur.fetchall():
        print("%6d %15s %7s %10s %10d %7s %10d "%(i[0],i[1],i[2],i[3],i[4],i[5],i[6]))
    print("-"*80)
def editaccount():
    accno=int(input("enter account:"))
    qry="select * from customer where accountno=%d"%(accno)
    cur.execute(qry)
    result=cur.fetchall()
    if len(result)>0:
       print("1 name")
       print("2 gender")
       print("3 email")
       print("4 phone number")
       ch=int(input("enter choice to modify the record:"))
       if ch==1:
           name=input("enter new name")
           qry="update customer set name='%s' where accountno=%d"%(name,accno)
       elif ch==2: 
          gen=input("enter gender")
          qry="update customer set gender='%s' where accountno=%d"%(gen,accno)
       elif ch==3:
           email=input("enter email")
           qry="update customer set email='%s' where accountno=%d"%(email,accno)   
       elif ch==4:
            phone=input("enter phone")
            qry="update customer set phone='%s' where accountno=%d"%(phone,accno)
       else:
            print("invalid input")
       if ch>=1 and ch<=4:
          cur.execute(qry)
          if cur.rowcount>0:
              print("record updated")
              con.commit()
          else:
               print("error in updating the record")
    else:
        print("invalid account number")
def DepositAmount():   
    ano=int(input("enter account number:"))
    qry="select balance_amt from customer where accountno=%d"%(ano)
    cur.execute(qry)
    result=cur.fetchall()
    if len(result)>0:
        amount=result[0][0]
        damount=int(input("enter amount to deposit:"))
        qry="update customer set balance_amt=%d where accountno=%d"%(amount+damount,ano)
        cur.execute(qry)
        qry="insert into transaction1 values(%d,'Credit','%s',%d)"%(ano,dt.datetime.now(),damount)
        cur.execute(qry)
        con.commit()
        if cur.rowcount>0:
           print("amount credited!!!")
        else:
            print("error in crediting the amount")
    else:
        print("invalid account number")
def ministatement():
    ano=int(input("enter account number:"))
    qry="select * from transaction1 where accountno=%d"%(ano)
    cur.execute(qry)
    result=cur.fetchall()
    if len(result)>0:
        print("-"*80)
        print("%7s %10s %15s %10s %10s"%("accountno","type","date","time","account"))
        print("-"*80)
        for i in result:
                date=i[2][0:10]
                time=i[2][11:19]
                print("%7d %10s %15s %10s %10s"%(i[0],i[1],date, time,i[3]))
                print("-"*90)
    else:
        print("no trasaction found...")
                
def withdrawAmount():   
    ano=int(input("enter account number:"))
    qry="select balance_amt from customer where accountno=%d"%(ano)
    cur.execute(qry)
    result=cur.fetchall()
    if len(result)>0:
        amount=result[0][0]
        wamount=int(input("enter amount to withdraw:"))
        if wamount<=amount:   
            qry="update customer set balance_amt=%d where accountno=%d"%(amount-wamount,ano)
            cur.execute(qry)
            qry="insert into transaction1 values(%d,'%s','%s',%d)"%(ano,"debit",dt.datetime.now(),wamount)

            cur.execute(qry)
            if cur.rowcount>0:
               print("amount withdraw!!!")
            else:
               print("error in crediting the amount")
            con.commit()              
        else:
           print("insufficient amount!!!!")
    else:
       print("invalid account number")
def showbalance():            
    ano=int(input("enter account number:"))
    qry="select balance_amt from customer where accountno=%d"%(ano)
    cur.execute(qry)
    result=cur.fetchall()
    if len(result)>0:
        amount=result[0][0]
        print("total account=",amount)
    else:
        print("invalid account number")
def closeAccount():
    ano=int(input("enter account number:"))
    qry="select balance_amt from customer where accountno=%d"%(ano)
    cur.execute(qry)
    result=cur.fetchall()
    if len(result)>0:
        qry="update customer set active=0 where accountno=%d"%(ano)
        cur.execute(qry)
        con.commit()
        print("account closed !!!!")
    else:
        print("invaild account number!!!!")

while True:
    os.system("cls")              
    print("%30s"%("banking management system"))
    print("1. create new account")
    print("2. deposit amount")
    print("3. withdraw amount")
    print("4. balance enquiry")
    print("5. view all account Holder")
    print("6. modify an account")
    print("7. mini system")
    print("8. close an account")
    print("9. exit")
    choice=int(input("enter choice:"))
    if choice==1:
        createAccount()               
    elif choice==2:
          DepositAmount()        
    
    elif choice==3:
            withdrawAmount()
        
    elif choice==4:
        showbalance()
       
    elif choice==5:
        viewallaccount()
        os.system("pause")             
    elif choice==6:
        editaccount()
    elif  choice==7:
        ministatement()           
    elif choice==8:
        closeAccount()
        
    elif choice==9:
        pass
    else:
        print("invalid choice.....")           
                    
                                   
                  
  

        
