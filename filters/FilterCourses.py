def merge_courses(original: dict[str, str], duplicate: dict[str, str]) -> bool:
    """Merge courses ORIGINAL and DUPLICATE, leaving the result in ORIGINAL.
    Returns a Boolean value which is True iff the merge was successful."""
    # Things to look at for the merge:
    #   - Which copy has a better name?  (How do you tell?)
    #   - Does one copy have an ARC code and the other not? done
    #   - Do they have different ARC codes? (don't merge!) done
    #   - Do the credit hours and grade codes match?

    # Check ARC codes first, to see whether to merge at all
    mergeable = True
    if len(original['ADV REQ CDE']) > 0 and len(duplicate['ADV REQ CDE']) > 0 \
        and original['ADV REQ CDE'] != duplicate['ADV REQ CDE']:
        mergeable = False

    if mergeable:
        # If original has no ARC but duplicate does, take the ARC
        if len(original['ADV REQ CDE']) == 0 and len(duplicate['ADV REQ CDE']) > 0:
            original['ADV REQ CDE'] = duplicate['ADV REQ CDE']
        
        # Take the longer name.  This is basically a WAG (no S), based on the
        # intuition that the longer name might be less abbreviated.
        if len(original['CRS TITLE']) < len(duplicate['CRS TITLE']):
            original['CRS TITLE'] = duplicate['CRS TITLE']

        if original['CREDIT HRS'] != duplicate['CREDIT HRS']:
            # Make a range.  Yes, there are floating-point values.
            new_hours = float(duplicate['CREDIT HRS'])
            if '-' in original['CREDIT HRS']:
                hour_strs = original['CREDIT HRS'].split('-')
                assert len(hour_strs) == 2, f"bad hour_strs: {hour_strs}"
                hours_low = float(hour_strs[0])
                hours_high = float(hour_strs[1])
            else:
                hours_low = float(original['CREDIT HRS'])
                hours_high = hours_low
            hours_low = min(hours_low, new_hours)
            hours_high = max(hours_high, new_hours)
            original['CREDIT HRS'] = f"{round(hours_low,2)}-{round(hours_high,2)}"            

        #     print('WARNING: Credit hours mismatch:')
        #     print(f'\t{original}')
        #     print(f'\t{duplicate}')

        # For right now, ignore GRADE CDE, TRANS YR, and TRANS TRM.

    return mergeable


def merge_duplicates(transfer_credits: list[dict[str,str]]) -> None:
    """Merges duplicate course entries in TRANSFER_CREDITS by side effect."""
    unique_courses: dict[str, int] = {}
    duplicates: list[int] = []
    hard_cases: list[tuple[dict[str,str], dict[str,str]]] = []
    for i in range(len(transfer_credits)):
        course = transfer_credits[i]
        key = f"{course['ORG CDE']}_{course['CRS CDE']}"
        if key not in unique_courses:
            unique_courses[key] = i
        else: # Duplicate.  Can they be merged?
            # print('\t',course)
            dup_course = transfer_credits[unique_courses[key]]
            # Double-check that the key matches
            assert key == f"{course['ORG CDE']}_{course['CRS CDE']}"
            assert key == f"{dup_course['ORG CDE']}_{dup_course['CRS CDE']}"
            if merge_courses(dup_course, course):
                # print(f'Duplicate course found for key "{key}":')
                duplicates.append(i)
            else:
                # course and dup_course had different ARC codes.
                # Try again, adding the ARC code, so we only have one copy with each ARC code
                key = f"{key}_{course['ADV REQ CDE']}"
                if key not in unique_courses:
                    unique_courses[key] = i
                else:
                    # We've seen this course before *with* this ARC code.
                    dup_course = transfer_credits[unique_courses[key]]
                    if merge_courses(dup_course, course):
                        # print(f'Duplicate course found for key "{key}":')
                        duplicates.append(i)
                    else:
                        print(f'Merge failed for key {key}: why?')
                        hard_cases.append((dup_course, course))
        assert len(hard_cases) == 0

    duplicates.reverse()
    for i in duplicates:
        #print('Deleting course', i)
        del transfer_credits[i]
    print(len(unique_courses), len(duplicates), len(hard_cases), len(transfer_credits))
        
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
         course_entry['CrsId'] = str(i)
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

    # Filter out any courses for which CREDIT TYPE CDE is not TR
    print(len(transfer_credits))
    for i in range(len(transfer_credits)-1, -1, -1):
        if transfer_credits[i]['CREDIT TYPE CDE'] != 'TR':
            # print('Deleting course with credit type',
            #       transfer_credits[i]['CREDIT TYPE CDE'])
            del transfer_credits[i]
    print(len(transfer_credits))

    # Regularize course codes
    for course in transfer_credits:
        course['CRS CDE'] = course['CRS CDE'].upper().replace(' ', '')

    # Merge duplicates (how do we figure out which copy has more data?)
    merge_duplicates(transfer_credits)

    # Clean up the names?  No.  Too hard.

    return make_course_data(transfer_credits)

# def filter_courses_old(transfer_credits: list[dict[str,str,str,str]]):
#     """Takes a list of dictionaries TRANSFER_CREDITS, with one entry per
#     course equivalence; merges the schools in the equivalence list and 
#     returns a list of dictionaries, each representing a unique school,
#     filtered to remove the schools we don't want."""
#     unique_names = set()
#     filtered_courses = []

#     # Now add the unique course names.
#     for record in transfer_credits:
#         course = record['CrsCode']

#         # Would this work? Ask team/Dr.Brown
#         if (course.split()).upper() not in unique_names:
#                 unique_courseHrs = set()
#                 if record['CreditHours'] not in unique_courseHrs:
#                     unique_courseHrs.add(courseHrs)
#                     unique_names.add((s.split()).upper())
#                     filtered_courses.append(record)
    
#     return filtered_courses