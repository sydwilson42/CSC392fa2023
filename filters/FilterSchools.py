def two_year(record: dict[str,str]) -> bool:
    """Returns True if the school in RECORD appears to be a 2-year
    school, based on our best SWAG's applied to its name."""
    junior = False  # Set to True if the school appears 2-year
    return junior

def filter_schools(transfer_credits: list[dict[str,str]]):
    """Takes a list of dictionaries TRANSFER_CREDITS, with one entry per
    course equivalence; merges the schools in the equivalence list and 
    returns a list of dictionaries, each representing a unique school,
    filtered to remove the schools we don't want."""
    unique_schools = set()
    filtered_schools = []

    # ID's of schools we don't want
    bad_schools = ['**0001', '**0002', '**0003', '**0004',  '**0006',
    #               AP        IB       'Unknown' 'Exemption' CLEP
                   '100089', '100251', 'INTL'  ]
    #               IB        IB        'International (Generic)'

    for record in transfer_credits:
        school = record['school']
        if school in bad_schools:
            # Will this work?
            del record
        elif school not in unique_schools:
            unique_schools.add(school)
            filtered_schools.append(record)
            
    return filtered_schools
