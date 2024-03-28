import re

def fix_name(orgname: str) -> str:
    replacements = {'C C': 'Community College',
                    'Cmty C': 'Community College',
                    'CC': 'Community College',
                    'Cc': 'Community College',
                    'Cmty Co': 'Community College',
                    'cmty coll': 'Community College',
                    'Col': 'College',
                    'Coll': 'College',
                    'Clg': 'College',
                    'Comm': 'Community',
                    'Cmty': 'Community',
                    'centrl': 'Central',
                    'I': 'Institute',
                    'Inst': 'Institute',
                    'Sch': 'School',
                    'St': 'State',
                    'TechnicalCollege': 'Technical College',
                    'U': 'University',
                    'Un': 'University',
                    'Univ': 'University',
                    # State names
                    'Il': 'Illinois',
                    'In': 'Indiana',
                    'Miss': 'Mississipi',
                    'Nc': 'North Carolina',
                    'Nj': 'New Jersey',
                    'Ny': 'New York',
                    'Pa': 'Pennsylvania',
                    'Sc': 'South Carolina',
                    'Tx': 'Texas',
                    'Ut': 'Utah',
                    'Va': 'Virginia',
                    #Acronyms
                    'Usc': 'University of South Carolina',
                    'Unc': 'University of North Carolina',
                    # Random stuff
                    'Centrl': 'Central',
                    'Vly': 'Valley',
                    'Intl': 'International',
                    'Sthrn': 'Southern',
                    'Cmps': 'Campus',
                    'N': 'North',}

    result = orgname.strip()
    # Remove strings of spaces
    result = result.replace('  ',' ')
    # Fails for reason not yet known
    for string in replacements.keys():
        result = re.sub(r'\b'+string+r'\b', replacements[string], result)

    return result

def two_year(record: dict[str,str]) -> bool:
    """Returns True if the school in RECORD appears to be a 2-year
    school, based on our best SWAG's applied to its name."""
    junior = False  # Set to True if the school appears 2-year
    return junior

def filter_schools(transfer_credits: list[dict[str,str]]):
    """Takes a list of dictionaries TRANSFER_CREDITS and SAT_CREDITS, with one entry per
    course equivalence; merges the schools in the equivalence list and 
    returns a list of dictionaries, each representing a unique school,
    filtered to remove the schools we don't want (while checking ceeb codes).  The original list of
    records is also filtered by side effect."""
    unique_schools = set()
    filtered_schools: list[dict[str,str]] = []

    # ID's of schools we don't want
    bad_schools = ['**0001', '**0002', '**0003', '**0004',  '**0006',
    #               AP        IB       'Unknown' 'Exemption' CLEP
                   '100089', '100251', 'INTL'  ,
    #               IB        IB        'International (Generic)'
                   '999995']
    #              "Comprehensive Exam"
    for record in transfer_credits:
        #print(record)
        school = record['ORG CDE']
        if school in bad_schools:
            # Will this work?
            del record
            continue
        # If this isn't a bad school
        # Pad 4-digit org codes with two leading zeroes because
        #   most of these codes appear to be 6 characters
        if len(school) == 4 and school.isdigit():
            school = '00' + school
        if school not in unique_schools:
            unique_schools.add(school)
            filtered_schools.append({'OrgCode': school,
                                     'College': fix_name(record['ORG NAME']),
                                     'TwoOrFourYear': two_year(record)})
            
    return filtered_schools

