import sqlite3
from pathlib import Path
from read_write_csv import read_from_csv

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

def create_insert_statement(table: str) -> str:
    records: list[dict[str,str]] = get_records(table)
    # Make an INSERT statement that insertes all the records into the table.
    # It will be a *very long* SQL string.  That's OK (I think, and if it isn't
    # OK, we'll split it up).
    return ';'

# Filenames, relative to CSC392FA2023
dbfilename = 'Transfer_DB.db'
CSV_dir = 'CSV Files'
tables = ['ARC', 'School', 'Course', 'Equivalence']

def get_records(table: str) -> list[dict[str, str]]:
    fname = table + 's.csv'
    records = read_from_csv(fname)
    assert len(records) > 0, f"No records in {fname}"
    print(f"{fname}: {len(records)} records")
    return records

def main(args: list[str]) -> int:
    dbfile = Path(dbfilename)
    assert dbfile.exists()
    conn = connectDB(dbfile)

    if conn:
        try:
            print(f'Connected to {dbfile}')
            # Clean out the old stuff
            for table in tables:
                with conn:
                    conn.execute(f'delete from {table};')

            # In with the new (from the CSV files)
            for table in tables:
                sql = create_insert_statement(table)
                with conn:
                    conn.execute(sql)

        finally:
            print('closing')
            closeDB(conn)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))