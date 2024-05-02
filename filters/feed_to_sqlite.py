import sqlite3

#Connect to the SQLite database
conn = sqlite3.connect('database file name') 
cursor = conn.cursor()

#Execute the SQL DELETE statement to delete all rows in a table
# cursor.execute("DELETE FROM table_name")
#(repeat this for all tables)

#Commit the statement
conn.commit()

#Close the connection
conn.close() 