import re

def read_canonical_name_list() -> list[dict[str,str]]:
    """Read the canonical name list and return it."""
    result: list[dict[str,str]] = []

    # Do the actual reading from csv here
    return result

canonical_name_list: list[dict[str,str]] = read_canonical_name_list()

def find_canonical_name(org_code: str) -> str:
    """Using the name database, find the canonical
    name for the school if it can be found.  If it
    can't be found, just return the empty string."""
    # Codes on the left should be mapped to codes on the right
    # Some mappings are already documented in Schools_compared.csv
    # Others you develop from schools_comparison.csv, as follows:
    #     - Look for the schools in schools_comparison.csv that have no CEEB or MDB equivalent
    #     - Search on the name.  If you find the name elsewhere in schools_comparison.csv,
    #           merge the unmatched on into the matched one.
    equivalences = {'*00016': '2519',
                    '***022': '001311',
                    '009917': '001311',
                    '$1 ': '005327'} # Just use the CEEB for name lookup
    ceeb = ''
    if org_code in equivalences:
        ceeb = equivalences[org_code]
    elif org_code.startswith('00'):
        ceeb = org_code[-4:]
    # If the CEEB can be found in the canonical_name_list,
    # get the name from there
    # Else, just return ''
    return ''

def fix_name(record: dict[str,str]) -> str:
    """Fix the school name.  First, look in the
    school name database, and get the name from there
    if possible.  If that is not possible, apply chewing
    gum, band-aids, and spit (the replacements heuristics)."""
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

    result = find_canonical_name(record['ORG CDE'])
    if result == '':
        result = record['ORG NAME'].strip()
        # Remove strings of spaces
        result = result.replace('  ',' ')
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
    merges = {'$1': '5327'} # Rewrite the OrgCode

    for record in transfer_credits:
        #print(record)
        school = record['ORG CDE']
        if school in bad_schools:
            # Will this work?
            del record
            continue
        # If this isn't a bad school
        elif school in merges:
            school = merges[school]
            record['ORG CDE'] = school
        #elif school in equivalences:
            # Figure out how to get the name right

        # Pad 4-digit org codes with two leading zeroes because
        #   most of these codes appear to be 6 characters
        if len(school) == 4 and school.isdigit():
            school = '00' + school
        if school not in unique_schools:
            unique_schools.add(school)
            filtered_schools.append({'OrgCode': school,
                                     'College': fix_name(record),
                                     'TwoOrFourYear': two_year(record)})
            
    return filtered_schools

