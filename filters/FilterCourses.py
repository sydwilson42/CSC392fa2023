def merge_courses(original: dict[str, str], duplicate: dict[str, str]) -> None:
    """Merge courses ORIGINAL and DUPLICATE, leaving the result in ORIGINAL.
    This is done unconditionally (The idea is to improve the quality of the data in ORIGINAL."""
    # Pre:
    assert original['ORG CDE'] == duplicate['ORG CDE'] and original['CRS CDE'] == duplicate['CRS CDE']
    # Things to look at for the merge:
    #   - Which copy has a better name?  (How do you tell?)
    #   - Does one copy have an ARC code and the other not? done
    #   - Do they have different ARC codes? (don't merge!) done
    #   - Do the credit hours and grade codes match?

    # If original has no ARC but duplicate does, take the ARC
    if len(original['ADV REQ CDE']) == 0 and len(duplicate['ADV REQ CDE']) > 0:
        original['ADV REQ CDE'] = duplicate['ADV REQ CDE']
    
    # Take the longer name.  This is basically a WAG (no S), based on the
    # intuition that the longer name *might* be less abbreviated.
    if len(original['CRS TITLE']) < len(duplicate['CRS TITLE']):
        original['CRS TITLE'] = duplicate['CRS TITLE']

    if original['CREDIT HRS'] != duplicate['CREDIT HRS']:
        # Make a range.  Yes, there are floating-point values in CREDIT HRS.
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
        if hours_low == int(hours_low):
            hours_low = int(hours_low)
        if hours_high == int(hours_high):
            hours_high = int(hours_high)
        original['CREDIT HRS'] = f"{hours_low}-{hours_high}"            

    # For right now, ignore GRADE CDE, TRANS YR, and TRANS TRM.


def merge_duplicates(transfer_credits: list[dict[str,str]]) -> dict[str, int]:
    """Merges duplicate course entries in TRANSFER_CREDITS by side effect.
    Returns a dictionary of unique courses, mapping a key to an index in 
    TRANSFER_COURSES.  To avoid fouling up the indices into TRANSFER_COURSES,
    duplicate courses are *not* deleted from TRANSFER_COURSES"""
    unique_courses: dict[str, int] = {}
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
            merge_courses(dup_course, course)

    print(len(unique_courses), len(transfer_credits))
    return unique_courses
        
def make_course_data(unique_courses: dict[str, int], transfer_credits: list[dict[str,str]]) -> list[dict[str,str|int]]:
    """Takes a list of dictionaries TRANSFER_CREDITS, with one entry
    per course equivalence.  TARNSFER_CREDITS is not modified here.
    Creates and returns a list of dictionaries representing the data for
    the Course table in the database."""
    # Develop the Course table dictionaries
    course_data: list[dict[str, str | int]] = []

    unique_keys = sorted(unique_courses.keys())
    for key in unique_keys:
        course_entry: dict[str, str | int] = {}
        course_entry['CrsId'] = unique_courses[key]
        course = transfer_credits[unique_courses[key]]
        course_entry['OrgCode'] = course['ORG CDE']
        course_entry['CrsCode'] = course['CRS CDE']
        course_entry['CrsName'] = course['CRS TITLE']
        course_entry['CreditHours'] = course['CREDIT HRS']
        course_entry['GrdCode'] = course['GRADE CDE']
        course_data.append(course_entry)
    
    return course_data

def filter_courses(transfer_credits: list[dict[str,str]]) -> list[dict[str,str | int]]:
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
    unique_courses = merge_duplicates(transfer_credits)

    # Clean up the names?  No.  Too hard.

    return make_course_data(unique_courses, transfer_credits)
