import sqlite3


# used to input a given table, and print out the rows and columns
def print_table(column_names, table):
    # printing the column names
    # using the description of the table
    i = 0
    print("-" * 30 * len(column_names))
    for column in column_names:
        if i == len(column_names) - 1:
            name = column[0]
            if column[0] == "tbl_name":
                name = "Table Names"
            center = name.center(28)
            print("|" + center, end="|")
            print()

        else:
            name = column[0]
            center = name.center(29)
            print("|" + center, end="")
        i += 1
    print("-" * 30 * len(column_names))

    for row in table:
        i = 0

        for col in row:
            col = str(col)
            if i == len(row) - 1:
                print("|" + col.center(28), end="|")
            else:
                print("|" + col.center(29), end="")
            i += 1
        print()
    print("-" * 30 * len(column_names))
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
            print("Invalid table choice")
            continue
        else:
            curr_table = conn.execute("SELECT * FROM " + table_choice)
            print_table(curr_table.description, curr_table)
            print()
            if not input("Press enter to exit"):
                done = True


def insert_row():
    # this will retrieve all of the table names in the db
    cursor = conn.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table'")

    table_names = cursor.fetchall()
    col_name = cursor.description
    print_table(col_name, table_names)

    done = False

    while not done:
        print("Choose a table to insert into from the list above (q to exit):")
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
            table_cols = curr_table.description

            # ------------------------------------------------------
            # this code is fetching the column data types for reference
            cursor.execute(f"PRAGMA table_info('{table_choice}');")
            column_info = cursor.fetchall()
            column_datatypes = [info[2] for info in column_info]
            colnames = "("
            i = 0
            for i in range(0, len(table_cols)):
                if i == len(table_cols) - 1:
                    colnames = colnames + table_cols[i][0] + ")"
                else:
                    colnames = colnames + table_cols[i][0] + ","
            # ------------------------------------------------------

            # print the column names

            print("Column Names:\n")

            print_table(table_cols, [])
            print("Enter the data you would like to enter for each column: \n")
            # request user input for each of the columns in the table to insert
            values = "("
            for i in range(0, len(table_cols)):
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
                print("Successfully inserted row with values: " + values)
                print()
                conn.commit()
                done = True
            except:
                print("row not successfully inserted")


def delete_entry():
    # this will retrieve all of the table names in the db
    cursor = conn.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table'")

    table_names = cursor.fetchall()
    col_name = cursor.description
    print_table(col_name, table_names)

    # getting the primary key from the table
    done = False

    while not done:
        print("Choose a table to delete from in the list above (q to exit):")
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
            table_cols = curr_table.description

            # get the primary key of the table as one row, one col
            pk_table = conn.execute(
                "SELECT l.name FROM pragma_table_info(\"" + table_choice + "\") as l WHERE l.pk = 1;")
            pktable = pk_table.fetchall()
            pk_string = pktable[0][0]
            print()
            print("The primary key column is: " + pk_string)

            # print the table they chose
            print_table(table_cols, curr_table)

            print()
            print("Please enter the Primary Key of the row you would like to delete:")
            key_in = input()

            # TODO: ADD DATA VALIDATION HERE

            try:
                curr = conn.execute("DELETE FROM " + table_choice + " WHERE " + pk_string + " = \'" + key_in + "\'")
                done = True
                conn.commit()
            except:
                print("deletion did not work")


def update_entry():
    # this will retrieve all of the table names in the db
    cursor = conn.execute("SELECT tbl_name FROM sqlite_master WHERE type = 'table'")

    table_names = cursor.fetchall()
    col_name = cursor.description
    print_table(col_name, table_names)

    # getting the primary key from the table
    done = False

    while not done:
        print("Choose a table to update from in the list above (q to exit):")
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
            table_cols = curr_table.description

            # get the primary key of the table as one row, one col
            pk_table = conn.execute(
                "SELECT l.name FROM pragma_table_info(\"" + table_choice + "\") as l WHERE l.pk = 1;")
            pktable = pk_table.fetchall()
            pk_string = pktable[0][0]
            print()
            print("The primary key column is: " + pk_string)

            # print the table they chose
            print_table(table_cols, curr_table)

            print()
            print("Please enter the column name you want to update")
            col_name = input()
            print("Please enter the value you would like to change the column to")
            update_val = input()
            print("Please enter condition to change")
            condition = input()

            try:
                curr = conn.execute("UPDATE " + table_choice + " SET " + col_name + "='"
                                    + update_val + "'WHERE " + condition)
                done = True
                conn.commit()
            except:
                print("update did not work")


def retrieval(statement):
    cursor = conn.execute(statement)
    table_names = cursor.fetchall()
    col_name = cursor.description
    print_table(col_name, table_names)


def other():
    global statement
    selected = False

    while not selected:
        print("1. View wins and losses of players")
        print("2. View wins by division")
        print("3. View a team's 3 point average")
        print("4. View all players correlated to all teams")
        print("5. View colleges that a player went to")
        print("6. View cities that have both a college and NBA team")
        print("q. Quit\n")

        user_in = input("Enter your selection: ")
        print()
        if user_in == "1":
            statement = "SELECT Player.Player_Name, Team.Wins, Team.Losses FROM Player " \
                        "INNER JOIN Team ON Player.Team_Name = Team.Team_Name"

        elif user_in == "2":
            division = input("Enter the division: ")
            statement = "SELECT Division.Division_Name, SUM(t1.Wins) FROM Division INNER JOIN Team as t1 " \
                        "ON t1.Division_Name = Division.Division_Name WHERE t1.Division_Name = '" + division + "' GROUP BY Division.Division_Name"

        elif user_in == "3":
            team = input("Enter the team: ")
            statement = "SELECT Player.Team_Name, AVG(Three_Point_Average) FROM Team " \
                        "INNER JOIN Player ON Player.Team_Name = '" + team + "'"

        elif user_in == "4":
            statement = "SELECT Player.Player_Name, Team.Team_Name FROM Player CROSS JOIN Team"

        elif user_in == "5":
            statement = "SELECT College_Name FROM College INTERSECT SELECT College_Name FROM WENT_TO"

        elif user_in == "6":
            statement = "SELECT Location FROM College INTERSECT SELECT Location FROM Team"

        elif user_in == "q":
            selected = True
        else:
            print("Invalid selection\n")
            continue
        retrieval(statement)

# create a connection to the database

conn = sqlite3.connect('nbastats.sl3', timeout=10)

# The return value of this is the table

print("---------------------------")
print("Welcome to NBA Stats")
print("---------------------------")
print()
done = False

while not done:
    print("1. Add a Row")
    print("2. Show Table")
    print("3. Update an Entry")
    print("4. Delete a Row")
    print("5. Other")
    print("q. Quit\n")

    user_in = input("Enter your selection: ")
    print()
    if user_in == "1":
        insert_row()
    elif user_in == "2":
        show_table()
    elif user_in == "3":
        update_entry()
    elif user_in == "4":
        delete_entry()
    elif user_in == "5":
        other()
    elif user_in == "q":
        done = True
    else:
        print("Invalid selection\n")
        continue
# close the connection
conn.close()
