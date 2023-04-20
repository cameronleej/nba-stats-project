import sqlite3
from tkinter import *
import tkinter

"""
#GUI setup
root = tkinter.Tk(className="nbastats")

def show_menu():
    # ALL OF THESE BELONG TO THE SHOW_FRAME
    clear_frames()
    user_input = StringVar()

    def get_user_input():
        return entry.get()

    input_title = Label(show_frame,text="Enter the table name you would like to view:")
    # Initialize a Label to display the User Input
    label = Label(show_frame, text="", font=("Courier 22 bold"))
    label.pack()
    input_title.pack()

    # Create an Entry widget to accept User Input
    entry = Entry(show_frame, width=40)
    entry.focus_set()
    entry.pack()

    my_input = tkinter.Button(show_frame, text="run", width=20, command=get_user_input).pack(pady=20)

    show_frame.pack()


def insert_menu():
    clear_frames()
    label = Label(insert_frame, text="Insert a row")
    label.pack()
    insert_frame.pack()


def clear_frames():

    for widgets in show_frame.winfo_children():
        widgets.destroy()
    show_frame.pack_forget()

    for widgets in insert_frame.winfo_children():
        widgets.destroy()
    insert_frame.pack_forget()


# set window size
root.geometry("800x450")

#set window color
root.configure(bg='#566173')

show_frame = Frame(root, width=800, height=450)
insert_frame = Frame(root, width=800, height=450,bg="blue")

menu_bar = Menu()
menu_bar.add_cascade(label="Show", command=show_menu)
menu_bar.add_cascade(label="Insert", command=insert_menu)

root.config(menu = menu_bar)


#main window loop
root.mainloop()
"""


#used to input a given table, and print out the rows and columns
def print_table(column_names, table):
    #printing the column names
    #using the description of the table
    i = 0
    for column in column_names:
        if i == len(column_names)- 1:
            print(column[0])
        else:
            print(column[0], end=", ")

        i += 1

    for row in table:
        i = 0
        for col in row:
            if i == len(row)- 1:
                print(col, end="")
            else:
                print(col, end=",")
            i += 1
        print()


def show_table():
    # this will retrieve all of the table names in the db
    cursor = conn.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table'")

    table_names = cursor.fetchall()
    col_name = cursor.description
    print_table(col_name, table_names)

    done = False

    while not done:
        print("Choose a table to show into from the list above (q to exit):")
        table_choice = str(input().strip())
        contains = False

        # checks to see if the name entered is a valid table name in db
        for row in table_names:
            for col in row:
                if col == table_choice:
                    contains = True
                    break

        if table_choice == "q":
            done = True
        elif not contains:
            print("invalid table choice")
            continue
        else:
            # user entered valid table name
            curr_table = conn.execute("SELECT * FROM " + table_choice)
            print_table(curr_table.description, curr_table)
            print()
            if not input("press enter to exit"):
                done = True


def insert_row():
    #this will retrieve all of the table names in the db
    cursor = conn.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table'")

    table_names = cursor.fetchall()
    col_name = cursor.description
    print_table(col_name, table_names)

    done = False

    while not done:
        print("Choose a table to insert into from the list above (q to exit):")
        table_choice = str(input().strip())
        contains = False

        #checks to see if the name entered is a valid table name in db
        for row in table_names:
            for col in row:
                if col == table_choice:
                    contains = True
                    break

        if table_choice == "q":
            done = True
        elif not contains:
            print("invalid table choice")
            continue
        else:
            #user entered valid table name
            curr_table = conn.execute("SELECT * FROM " + table_choice)
            table_cols = curr_table.description

            #------------------------------------------------------
            #this code is fetching the column data types for reference
            cursor.execute(f"PRAGMA table_info('{table_choice}');")
            column_info = cursor.fetchall()
            column_datatypes = [info[2] for info in column_info]
            colnames = "("
            i = 0
            for i in range(0,len(table_cols)):
                if i == len(table_cols) -1 :
                    colnames = colnames +  table_cols[i][0] + ")"
                else:
                    colnames = colnames + table_cols[i][0] + ","
            #------------------------------------------------------


            #print the column names
            print("Column names: ",end="")
            print_table(table_cols, [])

            #request user input for each of the columns in the table to insert
            values = "("
            for i in range(0,len(table_cols)):
                print(table_cols[i][0] + "(" + column_datatypes[i] + ")", end=": ")
                user_in = input()
                if column_datatypes[i][0] == "V":
                    if i == len(table_cols) - 1:
                        values = values + "'" + user_in + "')"
                    else:
                        values = values + "'" + user_in + "',"
                else:
                    if i == len(table_cols) - 1:
                        values = values + user_in + ")"
                    else:
                        values = values + user_in + ","

            try:
                cursor = conn.execute("INSERT INTO " + table_choice + " VALUES " + values + ";")
                print("row successfully inserted: " + values)
                print()
                conn.commit()
                done = True
            except:
                print("row not successfully inserted")


# create a connection to the database
conn = sqlite3.connect('nbastats.sl3', timeout=10)


#the return value of this is the table


print("Hello, welcome to NBA stats")
done = False

while not done:
    print("1. Insert row")
    print("2. Show table")
    print("3. Update an entry")
    print("4. Delete a row")
    print("5. Other")
    print("q. quit")

    user_in = input()

    if user_in == "1":
        insert_row()
    elif user_in == "2":
        show_table()
    elif user_in == "3":
        print("chose 3")
    elif user_in == "4":
        print("chose 4")
    elif user_in == "5":
        print("chose 5")
    elif user_in == "q":
        done = True
    else:
        continue


# close the connection
conn.close()





