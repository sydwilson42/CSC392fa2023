def filter_courses(transfer_credits: list[dict[str,str,str,str]]):
    """Takes a list of dictionaries TRANSFER_CREDITS, with one entry per
    course equivalence; merges the schools in the equivalence list and 
    returns a list of dictionaries, each representing a unique school,
    filtered to remove the schools we don't want."""
    unique_names = set()
    filtered_courses = []

    # Now add the unique course names.
    for record in transfer_credits:
        course = record['course']

        # Would this work? Ask team/Dr.Brown
        if (course.split()).upper() not in unique_names:
                unique_courseHrs = set()
                if courseHrs not in unique_courseHrs:
                    unique_courseHrs.add(courseHrs)
                    unique_names.add((s.split()).upper())
                    filtered_courses.append(record)
    
    return filtered_courses