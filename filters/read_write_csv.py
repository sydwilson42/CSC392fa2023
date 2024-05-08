from csv import DictReader, DictWriter, QUOTE_STRINGS
from pathlib import Path
#from typing import Any

this_file = Path(__file__)
csv_dir = Path(this_file.parent.parent, 'CSV Files')
#print(csv_dir)

def read_transfer_courses_csv() -> list[dict[str, str]]:
    """Read the original CSV file, and return its
    contents as a list of dictionaries."""
    original_CSV = Path(csv_dir, 'Transfer_Courses.csv')
    return read_from_csv(original_CSV)
    #print(original_CSV, original_CSV.exists())


# def read_sat_csv() -> list[dict[str, str]]:
#     """Read the original CSV file, and return its
#     contents as a list of dictionaries."""
    
#     return read_from_csv(original_CSV)

def read_from_csv(fname: str | Path) -> list[dict[str, str]]:
    """Read a CSV file FNAME, and return a list of dictionaries
    corresponding to its contents (one dictionary per line in the file).
    This function is deliberately generic.  If you want special-purpose
    functions, wrap this one, rather than changing it."""
    original_CSV = Path(csv_dir, fname)

    records: list[dict[str,str]] = []
    with open(original_CSV, 'r', newline='') as f:
        reader: DictReader[str] = DictReader(f)
        for row in reader:
            records.append(row)
    return records

def write_csv(fname: str, to_write: list[dict[str, str]]) -> None:
    headers = to_write[0].keys()
    write_file = Path(csv_dir, fname)
    with open(write_file, 'w', newline='') as f:
        writer = DictWriter(f, fieldnames=headers, quoting=QUOTE_STRINGS)
        writer.writeheader()
        for item in to_write:
            writer.writerow(item)