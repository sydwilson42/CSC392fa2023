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

def quote_val(string: str) -> str:
    result = string.strip()
    if len(result) == 0:
        result = '""'
    elif result[0] != '"' or result[-1] != '"':
        result = f'"{string}"'
    return result

def create_insert_statement(table: str) -> str:
    records: list[dict[str,str]] = get_records(table)
    # Make an INSERT statement that insertes all the records into the table.
    # It will be a *very long* SQL string.  That's OK (I think, and if it isn't
    # OK, we'll split it up).

    sql = f'INSERT INTO {table} '
    # Assumes all the rows have the same columns
    cols = '(' + ','.join(map(quote_val, records[0].keys())) + ')'
    #print(cols)
    sql += cols + ' VALUES '
    for record in records:
        vals = map(quote_val, record.values())
        val_string = "(" + ",".join(vals) + "), "
        sql += val_string

    #print(sql)
    #with open('School.csv') as fin:
    #    reader = csv.DictReader(fin)
    #    data = list(reader)
    #    to_db = [(i['col1'], i['col2']) for i in dr]
    #cur.execute("CREATE TABLE School (OrgCode, College, TwoOrFourYear);")

    #cur.execute("INSERT INTO School (OrgCode, College, TwoOrFourYear) VALUES (?, ?, ...);", to_db)
    #con.commit()
    #con.close()

    # Remove the last comma and add a semicolon
    return sql[:-2] + ';'

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
                print(sql)
                with conn:
                    conn.execute(sql)

        finally:
            print('closing')
            closeDB(conn)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))