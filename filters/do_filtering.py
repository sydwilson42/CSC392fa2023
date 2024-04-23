from read_write_csv import read_from_csv,write_csv
from FilterSchools import filter_schools
from FilterCourses import filter_courses
from FilterARCs import filter_arcs

def main(args: list[str]) -> int:
    original_records = read_from_csv('Transfer_Courses.csv')
    print(len(original_records), "records")

    # Filter the schools, 
    #     filtering the records from bad schools by side effect
    schools_list = filter_schools(original_records)
    # write the schools out
    write_csv('Schools.csv', schools_list)

    # Filter the courses, 
    #     filtering the records from bad courses by side effect
    course_list = filter_courses(original_records)
    # course_list uses indexes into original_records as course ID's.
    # Therefore, DO NOT DELETE RECORDS from original_records after
    # this point!

    # write the courses out
    write_csv('Courses.csv', course_list)

    # Filter the ARC's, by making a collection of unique ARC's.

    arcs_list = filter_arcs(original_records)

    # All an ARC needs, besides the ARC code itself, is the
    # credit type.  *IF* there's a valid credit type every time
    # we find a new ARC (there *should* be, but check before
    # assuming!), we can just add the new ARC to the list of
    # ARC's for the database as soon as we find a new one.
    
    # Write the ARC's
    write_csv('ARCs.csv', arcs_list)

    # Filter the equivalences.  This will need course_list as
    # well as original_records, because course_list has the
    # course ID's.
    # In original_records, a unique equivalence is represented
    # by a unique combination of org code, course code, and ARC.
    # Unique combinations of these three can be found in basically
    # the same way as we found unique combinations of org code and
    # course code in FilterCourses: make a dictionary with a 
    # concatenated string of f"{org code}_{course code}_{ARC}" as
    # the key and a dictionary with course ID and ARC code as the
    # value attached to each key.  Then you can tell if an org 
    # code/course code/ARC combination is unique by finding out whether
    # it's in the dictionary.
    
    # The course ID's can be found from course_list.  Note that the
    # course list is actually sorted in ascending order of org code,
    # and then in ascending order of course code within the org codes.
    
    # Write the equivalences

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main([]))

