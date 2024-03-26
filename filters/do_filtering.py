from read_write_csv import read_transfer_courses_csv, read_sat_csv ,write_csv
from FilterSchools import filter_schools

def main(args: list[str]) -> int:
    original_records = read_transfer_courses_csv()
    print(len(original_records), "records")

    # Filter the schools, filtering the records from bad schools by side effect
    schools_list = filter_schools(original_records)
    # write the schools out
    write_csv('Schools.csv', schools_list)

    # Filter the courses
    # write the courses out

    # Filter the ARC's
    # Write the ARC's

    # Filter the equivalences
    # Write the equivalences

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main([]))

