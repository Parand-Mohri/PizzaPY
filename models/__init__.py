import mysql.connector

mydb = mysql.connector.connect(host= "localhost", user="root", passwd="", database="pizza")

print(mydb)

if(mydb):
    print("database is connected")
else:
    print("database is not connected")