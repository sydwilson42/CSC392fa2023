def merge_duplicates(transfer_credits: list[dict[str,str]]) -> None:
    """Merges duplicate course entries in TRANSFER_CREDITS by side effect."""
    unique_courses: dict[str, int] = {}
    num_dups = 0
    num_easy = 0
    i = 0
    for course in transfer_credits[:100]:
        key = course['ORG CDE'] + '_' + course['CRS CDE'] # Should be unique
        if key not in unique_courses:
            unique_courses[key] = i
        else: # Duplicate.  Can they be merged?
            num_dups += 1
            dup_course = transfer_credits[unique_courses[key]]
            print(f'Duplicate course found for key "{key}":')
            print('\t',dup_course)
            print('\t',course)
            # Things to look at for the merge:
            #   - Which copy has a better name?  (How do you tell?)
            #   - Does one copy have an ARC code and the other not?
            #   - Do they have different ARC codes? (don't merge!)
            #   - Do the credit hours and grade codes match?


        i += 1


            # print('Duplicate course found:')
            # print('\t',transfer_credits[unique_courses[key]])
            # print('\t',transfer_credits[i])
    print(len(unique_courses), num_dups, num_easy, len(transfer_credits))
        
def make_course_data(transfer_credits: list[dict[str,str]]) -> list[dict[str,str]]:
    """Takes a list of dictionaries TRANSFER_CREDITS, with one entry
    per course equivalence.  TARNSFER_CREDITS is not modified here.
    Creates and returns a list of dictionaries representing the data for
    the Course table in the database."""
    # Develop the Course table dictionaries
    course_data: list[dict[str, str]] = []
    i = 1
    for course in transfer_credits:
         course_entry: dict[str, str] = {}
         course_entry['CrsId'] = i
         course_entry['OrgCode'] = course['ORG CDE']
         course_entry['CrsCode'] = course['CRS CDE']
         course_entry['CrsName'] = course['CRS TITLE']
         course_entry['CreditHours'] = course['CREDIT HRS']
         course_entry['GradeCode'] = course['GRADE CDE']
         course_data.append(course_entry)
         i += 1
    return course_data

def filter_courses(transfer_credits: list[dict[str,str]]) -> list[dict[str,str]]:
    """Takes a list of dictionaries TRANSFER_CREDITS, with one entry
    per course equivalence.  Any merging of schools is assumed to have
    happened already.  This function merges duplicate courses and
    filters out bad courses in TRANSFER_CREDITS by side effect.  This
    function returns a list of dictionaries representing the data for
    the Course table in the database."""

    # Regularize course codes
    for course in transfer_credits:
        course['CRS CDE'] = course['CRS CDE'].upper().replace(' ', '')

    # Merge duplicates (how do we figure out which copy has more data?)
    merge_duplicates(transfer_credits)

    # Clean up the names?

    return make_course_data(transfer_credits)

def filter_courses_old(transfer_credits: list[dict[str,str,str,str]]):
    """Takes a list of dictionaries TRANSFER_CREDITS, with one entry per
    course equivalence; merges the schools in the equivalence list and 
    returns a list of dictionaries, each representing a unique school,
    filtered to remove the schools we don't want."""
    unique_names = set()
    filtered_courses = []

    # Now add the unique course names.
    for record in transfer_credits:
        course = record['CrsCode']

        # Would this work? Ask team/Dr.Brown
        if (course.split()).upper() not in unique_names:
                unique_courseHrs = set()
                if record['CreditHours'] not in unique_courseHrs:
                    unique_courseHrs.add(courseHrs)
                    unique_names.add((s.split()).upper())
                    filtered_courses.append(record)
    
    return filtered_courses