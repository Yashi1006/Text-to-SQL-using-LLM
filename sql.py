import sqlite3

##connect
connection = sqlite3.connect("student.db");

##cursor creation
cursor = connection.cursor()

##table creation
table_info = """ 
CREATE TABLE Employees (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Department TEXT NOT NULL,
    Salary INTEGER NOT NULL,
    Hire_Date TEXT NOT NULL);
"""

cursor.execute(table_info)

##insert records
cursor.execute('''INSERT INTO Employees VALUES(1, 'Alice', 'Sales', 50000, '2021-01-15')''')
cursor.execute('''INSERT INTO Employees VALUES(2, 'Bob', 'Engineering', 70000, '2020-06-10')''')
cursor.execute('''INSERT INTO Employees VALUES(3, 'Charlie', 'Marketing', 60000, '2022-03-20')''')

##Display all records
print("inserted records are")

data = cursor.execute('''SELECT * From Employees''')

for row in data:
    print(row)

##table2 creation
table_info = """ 
CREATE TABLE Departments (
    ID INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    Manager TEXT NOT NULL);
"""

cursor.execute(table_info)

##insert records
cursor.execute('''INSERT INTO Departments VALUES(1, 'Sales', 'Alice')''')
cursor.execute('''INSERT INTO Departments VALUES(2, 'Engineering', 'Bob')''')
cursor.execute('''INSERT INTO Departments VALUES(3, 'Marketing', 'Charlie')''')

##Display all records
print("inserted records are")

data = cursor.execute('''SELECT * From Departments''')

for row in data:
    print(row)

##close connection
connection.commit()
connection.close()