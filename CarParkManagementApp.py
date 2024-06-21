import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector

#connect to the database
mydb=mysql.connector.connect(host='127.0.0.1',
                     user='root',
                     passwd='MySQL', 
                     db='assessment3')

# apply SQL
pointer=mydb.cursor()

# Main window
root = tk.Tk()
root.title('MP Student Car Park App')
root.geometry('600x450')

# Treeview
tree = ttk.Treeview(root, columns=(1, 2, 3, 4, 5), show='headings', height=8)
tree.pack()

# eadings
tree.heading(1, text='student ID')
tree.heading(2, text='firstname')
tree.heading(3, text='lastname')
tree.heading(4, text='campus')
tree.heading(5, text='car number')

# Column width
tree.column(1, width=100)
tree.column(2, width=100)
tree.column(3, width=100)
tree.column(4, width=100)
tree.column(5, width=100)

#show data in the database
pointer.execute('SELECT * FROM assessment3.student')
# fetch all the data
data = pointer.fetchall()
for i in data:
    tree.insert('', 'end', values=i)

#student list 
sList=[]

def select_data():
    #clear entry boxes
    sID.delete(0,'end')
    sFN.delete(0,'end')
    sLN.delete(0,'end')
    campus.current(0)
    car.delete(0,'end')
    

def AddData():
    sID_value=(sID.get())
    sFN_value=(sFN.get())
    sLN_value=(sLN.get())
    campus_value=(campus.get())
    car_no=(car.get())
    
    myList=(sID_value, sFN_value, sLN_value, campus_value, car_no)

    #insert data into tree
    if sID_value.isdigit() == False:
        messagebox.showerror('showerror', 'Invalid input.' + '\n' + 'Please re-enter your ID as number.')
        return
    
    elif len(sID_value) != 7:
        messagebox.showerror('showerror', 'Invalid input.' + '\n' + 'Please re-enter your ID (7 numbers).')
        return

    elif sFN_value.isalpha() == False:
        messagebox.showerror('showerror', 'Invalid input.' + '\n' + 'Invalid input. ' + '\n' + 'Please re-enter your Firstname as alphabet.')
        return

    elif sLN_value.isalpha() == False:
        messagebox.showerror('showerror', 'Invalid input.' + '\n' + 'Invalid input. ' + '\n' + 'Please re-enter your Lastname as alphabet.')
        return

    else:
        sID_value= int(sID_value)
        insert= '''INSERT INTO assessment3.student (StudentID, FirstName, LastName, Campus, CarRegisNo)\
                    VALUES(%s, %s, %s, %s, %s)''' 
        pointer.execute(insert, myList)
        mydb.commit()
        select_data()
        tree.insert('', 'end', values=myList)
        sList.append(myList)
        
        
def SortData():
    # remove existing rows from the Treeview
    tree.delete(*tree.get_children())
    
    # sort data in database
    sort_db = 'SELECT * FROM student ORDER BY StudentID'
    pointer.execute(sort_db)
    
    # insert the sorted rows into the Treeview
    for row in data:
        tree.insert('', 'end', values=row)
    
    
def FindData():
    sID_value = sID.get()
    match = 'SELECT * FROM student WHERE StudentID = %s'
    pointer.execute(match, (sID_value,))
    #fetch the data matched
    result = pointer.fetchone()

    if result is not None:
        tree.delete(*tree.get_children())
        tree.insert('', 'end', values=result)
        
    else:
        messagebox.showerror('showerror', 'Your ID is not registered.')


#student ID label
studentID=ttk.Label(root, text='Student ID', font='Arial 10').place(x=120, y=200)
#entery widget
sID=ttk.Entry(root, width=19)
sID.place(x=210, y=200)

#fistname label
firstname=ttk.Label(root, text='Firstname', font='Arial 10').place(x=120, y=230)
#entery widget
sFN=ttk.Entry(root, width=41)
sFN.place(x=210, y=230)

#lastname label
lastname=ttk.Label(root, text='Lastname', font='Arial 10').place(x=120, y=260)
#entery widget
sLN=ttk.Entry(root, width=41)
sLN.place(x=210, y=260)

#campus dropdown menu
location=ttk.Label(root, text='Campus', font='Arial 10').place(x=120, y=290)
#option widget
campus= ttk.Combobox(root, width=39, values=['Preston', 
                                             'Collinwood',
                                             'Epping',
                                             'Heidelberg',
                                             'Prahran',
                                             'Greensborough',
                                             'Broadmeadows',
                                             'Eden park', 
                                             'Yan Yean', 
                                             'Ararat'])
campus.current(0)
campus.place(x=210, y=290)

#car registration label
carregisno=ttk.Label(root, text='Car No.', font='Arial 10').place(x=120, y=320)
#entery widget
car=ttk.Entry(root, width=41)
car.place(x=210, y=320)

# Button
search=ttk.Button(root, text='SEARCH NAME', width=18, command=FindData).place(x=340, y=195)
add=ttk.Button(root, text='ADD', width=25, command=AddData).place(x=120, y=360)
sort=ttk.Button(root, text='SORT BY ID', width=25, command=SortData).place(x=300, y=360)

# Style
style = ttk.Style()
style.theme_use('default')
style.map('Treeview')


root.mainloop()

mydb.close()