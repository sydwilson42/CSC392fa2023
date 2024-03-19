from read_write_csv import read_from_csv
from FilterSchools import filter_schools
from FilterCourses import filter_courses

def main(args: list[str]) -> int:
    records = read_from_csv()
    print(len(records), "records")

    # Filter the schools
    schools_list = filter_schools(records)
    # write the schools out

    # Filter the courses
    courses_list = filter_course(records)
    # write the courses out

    # Filter the ARC's
    # Write the ARC's

    # Filter the equivalences
    # Write the equivalences

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main([]))

