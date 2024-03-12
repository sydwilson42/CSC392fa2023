from pathlib import Path
from csv import DictReader, DictWriter

this_file = Path(__file__)
csv_dir = Path(this_file.parent.parent, 'CSV Files')
#print(csv_dir)

def read_from_csv() -> list[dict[str, str]]:
    """Read the original CSV file, and return its
    contents as a list of dictionaries."""
    original_CSV = Path(csv_dir, 'Transfer_Courses.csv')
    #print(original_CSV, original_CSV.exists())

    records: list[dict[str,str]] = []
    with open(original_CSV, 'r') as f:
        reader: DictReader = DictReader(f)
        for row in reader:
            records.append(row)
    return records

def write_csv(fname: str, to_write: list[dict[str, str]]) -> None:
    headers = to_write[0].keys()
    write_file = Path(csv_dir, fname)
    with open(write_file, 'w') as f:
        writer = DictWriter(f, fieldnames=headers)
        writer.writeheaders()
        for item in to_write:
            writer.writerow(item)