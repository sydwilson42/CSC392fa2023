import sqlite3
from pathlib import Path

def connectDB(db_fname: Path) -> sqlite3.Connection:
    #Connect to the SQLite database
    conn = sqlite3.connect(db_fname) 
    return conn

def getCursor(conn: sqlite3.Connection) -> sqlite3.Cursor:
    return conn.cursor()

#Execute the SQL DELETE statement to delete all rows in a table
# cursor.execute("DELETE FROM table_name")
#(repeat this for all tables)

def closeDB(conn: sqlite3.Connection) -> None:

    #Close the connection
    conn.close() 

def main(args: list[str]) -> int:
    conn = connectDB


    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))