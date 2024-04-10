from read_write_csv import read_from_csv,write_csv
#from FilterSchools import filter_schools
from FilterCourses import filter_courses

def main(args: list[str]) -> int:
    original_records = read_from_csv('Transfer_Courses.csv')
    print(len(original_records), "records")

    # Filter the schools, 
    #     filtering the records from bad schools by side effect
    #schools_list = filter_schools(original_records)
    # write the schools out
    #write_csv('Schools.csv', schools_list)

    # Filter the courses, 
    #     filtering the records from bad courses by side effect
    course_list = filter_courses(original_records)
    # write the courses out
    write_csv('Courses.csv', course_list)

    # Filter the ARC's
    # Write the ARC's

    # Filter the equivalences
    # Write the equivalences

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main([]))

