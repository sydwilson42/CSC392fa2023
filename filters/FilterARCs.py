ARC_equivalences = {'ART0101': 'ART100',
                    'BA330': 'BAD330', # Mgmt principles
                    'BIOL101': 'BIO101',
                    'BIOL205': 'BIO205', # Anatomy & Phys, with lab
                    'BIOL210': 'BIO210', # Antomy & Phys II, with lab
                    'CS100': 'CSC100', # Why is this an ARC?
                    'ECO202': 'ECN202',
                    'EN101': 'ENG101',
                    'EN102': 'ENG102',
                    'EN204': 'ENG204',
                    'ENG0101': 'ENG101',
                    'ENG0102': 'ENG102', # Seem to be some comp courses here?
                    'ENG1102': 'ENG102', # Comp course?
                    'ENGL102': 'ENG102', # Comp course
                    'ENGLU101': 'ENG101',
                    'FLG001': 'SPN101', # Only occurs with Spanish
                    'FOLA201': 'JPN201', # Only occurs with Japanese
                    'FREN102': 'FRN102', # Elementary French
                    'FREN201': 'FRN201', # More French
                    'FRLGN001': 'ASL101', # Only happens with ASL

                    # GEP COURSES:
                    # GE211 - humanities
                    # GEP1, GEP1E, GEP1F - history
                    # GEP1A, GEP1B - music
                    # GEP1G - religion
                    # GEP1H - women's studies
                    # GEP1I - ethics/philosophy
                    # GEP1J - biology/physiology
                    # GEP1K - chemistry
                    # GEP1L - physics
                    # GEP1M - geology
                    # GEP1N - sociology
                    # GEP1O - psychology
                    # GEP1P - microeconomics
                    # GEP1Q - politics/government
                    # GEP1W - nutrition
                    # GEP2 - math/algebra
                    # GEP2A - math/precalculus
                    # GEP2P - macroeconomics
                    # GEP3 - random science
                    # GEP3A - random arts/humanities
                    # GEP3B - random history
                    # GEP3C - random human geography
                    # GEP3E - environmental science
                    # GEP3N, GEP3X - world history                    

                    # HPE COURSES:
                    # REPLACE THESE WITH HPE134?
                    # HPE001 - field hockey
                    # HPE100 - equestrian
                    # HPE130 - basketball
                    # HPE132 - soccer
                    # HPE134 - volleyball

                    # OTHER COURSES:
                    # HRP101, HRP103, HRP201 - harp
                    # JPN101, JPN102, JPN202 - japanese
                    # LAT101, LAT102 - latin

                    'HIS106':'HST201',
                    'HIS108':'HST202',
                    'HIS201':'HST201',
                    'HIS202':'HST202',
                    'HIST201':'HST201',
                    'HIST202':'HST202',
                    'HLTH140':'HPE180',
                    'HPE00':'HPE151', #replace jogging with walk/swim?
                    'HPE120':'HPE126', #replace with tennis course
                    'HPE197':'HPE255', #replace with health and wellness
                    'HPE224':'HPE124', #replace with golf
                    'HST00':'HST100', #double check
                    'HST001':'HST115', #double check
                    'HST101':'HST201', #double check
                    'HST102':'HST100', #double check
                    'HST188':'HST115', #double check
                    'HST315':'HST115', #double check
                    'HST318':'HST110', #double check
                    'HST319':'HST100', #double check
                    'HST599':'HST110', #double check
                    'MA202':'MTH108',
                    'MAT101':'MTH423',
                    'MAT108':'MTH423',
                    'MAT110':'MTH112',

                    'MATH108': 'MTH108',
                    'MATH110': 'MTH110',
                    'MATH1113': 'MTH113',
                    'MATH113': 'MTH113',
                    'MATH115': 'MTH115', # Calculus One
                    'MATH221': 'MTH120', # Analytical Geometry & Calculus
                    'MTH00': 'MTH110', # Elementary Functions
                    'MTH11': 'MTH105', # College Algebra
                    'POL100': 'POL101', # US Government & Politics
                    'PS101': 'PSY101', # General Psychology
                    'PSY00': 'PSY101', # General Psychology
                    'SOC00': 'SOC101', # Intro to Sociology
                    'SOC0101': 'SOC101', # Intro to Sociology
                    'SPA101': 'SPN101', # Elementary Spanish I
                    'SPA102': 'SPN102', # Elementary Spanish II
                    'SPA201': 'SPN201', # Intermediate Spanish
                    'SPA202': 'SPN202', # Intermediate Spanish
                    'SPAN201': 'SPN201', # Intermediate Spanish I
                    'SPAN202': 'SPN202', # Spanish IV
                    'THE1000': 'THR100', # Intro to Theatre
                    'THE1150': 'THR115', # Fundamentals of Acting
                    'TRANS001': 'TRAN001' # "Transfer Work"
                    }

def filter_arcs(transfer_credits: list[dict[str,str]]) -> list[dict[str,str]]:
    """Takes a list of dictionaries TRANSFER_CREDITS, with one entry
    per course equivalence.  Any merging of schools is assumed to have
    happened already. Any merging of courses is assumed to have
    happened already. This function merges bogus ARC codes in
    TRANSFER_CREDITS by side effect, but does not remove any entries.
    This function returns a list of dictionaries representing the data
    for the ARCs table in the database."""

    unique_ARCs: set[str] = set[str]() # Used to test for uniqueness
    filtered_ARCs: list[dict[str, str]] = [] # This goes in the database
    for record in transfer_credits:
        ARC_code = record['ADV REQ CDE'].upper().replace(' ', '')
        if ARC_code in ARC_equivalences:
            ARC_code = ARC_equivalences[ARC_code]
            record['ADV REQ CDE'] = ARC_code
            # Remains to be seen whether this leads to duplicate equivalences
        credit_type = record['CREDIT TYPE CDE']
        if len(ARC_code) > 0: # Get rid of the empty ARCs
            if ARC_code not in unique_ARCs:
                assert credit_type == 'TR', \
                    f"{credit_type}: {record['ORG CDE']} {record['CRS CDE']} {ARC_code}"
                unique_ARCs.add(ARC_code)
                filtered_ARCs.append({'ARCCode' : ARC_code})

    # Bogus ARC for the equivalences that don't have an ARC
    filtered_ARCs.append({'ARCCode': 'Elective credit'})
    filtered_ARCs.sort(key=lambda elt: elt['ARCCode']) # sort by ARC
    return filtered_ARCs
