from pathlib import Path
from csv import DictReader, DictWriter

this_file = Path(__file__)
csv_dir = Path(this_file.parent.parent, 'CSV Files')
#print(csv_dir)

def read_transfer_courses_csv() -> list[dict[str, str]]:
    """Read the original CSV file, and return its
    contents as a list of dictionaries."""
    original_CSV = Path(csv_dir, 'Transfer_Courses.csv')
    #print(original_CSV, original_CSV.exists())

    records: list[dict[str,str]] = []
    with open(original_CSV, 'r', newline='') as f:
        reader: DictReader = DictReader(f)
        for row in reader:
            records.append(row)
    return records

def read_sat_csv() -> list[dict[str, str]]:
    """Read the original CSV file, and return its
    contents as a list of dictionaries."""
    original_CSV = Path(csv_dir, 'sat-score-reporting-code-list-working.csv')

    records: list[dict[str,str]] = []
    with open(original_CSV, 'r', newline='') as f:
        reader: DictReader = DictReader(f)
        for row in reader:
            records.append(row)
    return records

def write_csv(fname: str, to_write: list[dict[str, str]]) -> None:
    headers = to_write[0].keys()
    write_file = Path(csv_dir, fname)
    with open(write_file, 'w', newline='') as f:
        writer = DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for item in to_write:
            writer.writerow(item)