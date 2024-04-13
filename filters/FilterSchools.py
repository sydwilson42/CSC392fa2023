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
    equivalences = {'$00001': '005327', # Ai Miami Intl University of Art & Design -> Miami International Universit of Art and Design
                    '****UC': '007181', # University of Cambridge to Cambridge University
                    '***018': '005546', # Los Angeles Valley College
                    '***020': '007585', # "Sch of Prof Studies - University Cntr" should be CUNY's, since they have a University Center
                    '***021': '003708', # Keiser University - MelbourneCampus
                    '***022': '003825', # Ivy Tech Community College
                    '***024': '002785', # Jones International University
                    '**0000': '005078', # Coastal Georgia Community College, now College of Coastal Georgia
                    '**0007': '006874', # University of Minnesota - Twin Cities
                    '**0015': '006000', # American Public University System
                    '**0016': '005638', # Saint Leo University
                    '**0019': '000946', # InterAmerican University of Puerto Rico
                    '**0020': '005120', # Concord University
                    '**0025': '001325', # Indiana University-Indianapolis
                    '**025': '006591',  # Universidad de Monterrey
                    '**5711': '005711', # Georgia Perimeter College
                    '**0NIU': '001090', # Northeastern Illinois University
                    '**AASU': '005012', # Armstrong Atlantic State University
                    '**Amer': '000866', # American University of Paris
                    '**ART': '003463',  # Art Institute of California-Hollywood
                    '**ASTU': '005406', # Augusta State University, now Augusta University
                    '**CALU': '004088', # California Lutheran College, now California Lutheran University
                    '**CHIN': '005690', # Chinese University of Hong Kong
                    '**COVE': '006124', # Covenant College
                    '**ECPI': '003145', # ECPI College of Technology - Greenville
                    '**PURD': '001631', # Purdue University
                    '**TUCC': '006839', # Tulsa Community College
                    '**UNCS': '005512', # University of NC School of the Arts
                    '**UMCP': '005814', # University of Maryland College Park
                    '*00016': '002519', # The College of New Jersey
                    '*00017': '003829', # Capella University
                    '*0009': '005848',  # Kaplan University, now Purdue University 
                    '000346': '001738', # Troy State University Dothan, now Troy University
                    '000389': '006850', # University of Texas at Tyler
                    '000457': '003623', # South Piedmont Community College
                    '000970': '004381', # University of La Verne Athens
                    '001420': '004007', # Arizona State University
                    '001510': '005526', # Northwest Florida State College
                    '001547': '005029', # Point University
                    '001601': '005900', # University of West Georgia
                    '001643': '001154', # Spoon River College (mismatch)
                    '002063': '005137', # Community College of Baltimore County (used MDB code).  Note collision with Borough of Manhattan CC, below.
                    '002255': '002263', # Fairleigh Dickinson Rutherford, to main campus
                    '002691': '002063', # Borough of Manhattan Community College (used FICE code)
                    '002736': '002765', # Rutgers University School of the Arts -> Rutgers University
                    '002940': '002927', # University of Pittsburgh Gnstd (= General Studies)
                    '002954': '005534', # University of North Carolina (Pembroke)
                    '003030': '001088', # Ohio Christian University (used MDB code)
                    '003224': '003465', # Johnson & Wales University (assuming main campus)
                    '003408': '003733', # Community College of Rhode Island (some entries used the FICE code)
                    '004365': '005515', # Northern Virginia Community College
                    '005032': '005226', # Tidewater Community College
                    '005036': '005074', # Broward Community College, Central (note collision with Embry-Riddle)
                    '005193': '005137', # Essex Community College, now part of Community College of Baltimore County 
                    '005336': '005406', # Augusta College, now Augusta University
                    '005347': '005340', # J. Sargeant Reynolds Community College
                    '005465': '005457', # Miami Dade Community College, now Miami Dade College
                    '005562': '005569', # Pasco-Hernando Community College, now Pasco-Hernando State College
                    '006729': '006694', # San Jacinto College: North merged into the rest of San Jacinto College
                    '006933': '005863', # "Voorhess College" doesn't exist, but Voorhees College (now University) does
                    '007102': '003608', # CAD Institute, now University of Advancing Technology
                    '007354': '006904', # Athabasca University
                    '008308': '005091', # Cecil Community College
                    '008660': '005276', # Germanna Community College
                    '009917': '003825', # Ivy Tech Community College
                    '009976': '003619', # College of the Ouachitas
                    '01293': '004701',  # Vanguard University
                    '021002': '006070', # Dallas College
                    '031229': '003990'  # York County Community College
                    } 
     # Just use the CEEB for name lookup
    # Note: ***NOT FINISHED*** Check schools (ones I cannot find distinct/clear/any CEEB codes for): 
    # Sherman College of Chiropractic [leave separate], 
    # Edexcel Limited, [British examination company.  No CEEB, as far as I know.  Leave it separate.]
    # University of Belgrano, [In Argentina.  Leave it separate.]
    # Maricopa Community College [fixed name], 
    # Rockport College [leave separate--now Maine Media College, with no CEEB],
    # Institute Int’l Educ of Sch, [There are several around Europe.  No idea which this is.  Fixed the name.]
    # Presbyterian Univ-Mackenzie (Brazil), [It's in Brazil.  Leave it separate.]
    # Metropolitan Community College, [We have no way to tell which is which.  Leave it separate for the moment.]
    # Demoratic Socialist Republic of Sri Lanka, [Leave it separate.]
    # University of Madras, [In India.  Leave it separate.]
    # Al al-Bayt University -Jordan, [Leave it separate.]
    # Baylor College of Medicine, [No CEEB, and no affiliation with Baylor University.  Leave it separate.]
    # Bavarian State Ministry, [Leave it separate.]
    # Goethe Institut, [In Frankfurt, Germany.  Leave it separate.]
    # Italiaidea, [Can't find it.  Leave it separate.]
    # Open Universities Australia, [leave it separate]
    # Universite Montpellier II, [leave it separate]
    # University of Malaga - Spain, [leave it separate]
    # University of Salamanca, [leave it separate]
    # Moscow State Academy of PE, [Not sure.  Probably Russian.  Leave it alone.]
    # University of the West Indies, [In Trinidad & Tobago, from MDB.  Leave it separate.]
    # Institute for American University, [French, according to the MDB.  Leave it alone.]
    # Voronezh State University, [Russian.  Leave separate; no CEEB code of 1000]
    # Barat Coll, [acquired by DePaul U. 2001, closed 2005; leave it separate]
    # University of Fine Arts & Design Ganexa, [leave it be for now]
    # Westminster Choir Co [leave separate.  Purchased by--but not fully integrated into--Rider University.]

    # Marymount College Ny [Defunct.  Bought by Fordham 2005, shut down 2008.  Leave be.]
    # American Armn Intl C [Looks like it should be the American-Armenian International College, but I can find no trace of it.  Leave it be.]
    # Edison Community College, CEEB 005191, is *not* a mismatch.  It was a Florida college, now Florida SouthWestern State College.
    # Floyd College, CEEB 005237, really is now Georgia Highlands College.
    # Dixie Academy [Predecessor school, 1913-1916, of Utah Tech University.  Given the dates, the identification seems shaky.  Leave be.]
    # Salina Area Vocational Tech Sc [No CEEB.  Name fixed.]
    # Charles University [In Czechia.  Leave separate.]
    # Washoe High School [leave separate]
    # Tampines Junior College [Leave separate: defunct.]
    # Anhui Medical University [Chinese, no CEEB.  Leave separate.]
    # CAEL [Canadian Academic English Language Assessment, a Canadian English-proficiency test.  No CEEB.  Leave it be.]

    # Ask Dr. Brown if we are reading in the course codes from Transfer_Courses.csv. Make sure codes match up. 

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
    replacements = {# Entire names
                    'Institute Int’l Educ of Sch': 'Institute of International Educational Studies',
                    'Maricopa Community College': 'Maricopa County Community College District',
                    'Salina Area Vocational Tech Sc': 'Salina Area Technical College',        
                    # Common abbreviations
                    'C C': 'Community College',
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
                    'N': 'North'
                    }

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

def filter_schools(transfer_credits: list[dict[str,str]]) -> list[dict[str,str]]:
    """Takes a list of dictionaries TRANSFER_CREDITS and SAT_CREDITS, with one entry per
    course equivalence; merges the schools in the equivalence list and 
    returns a list of dictionaries, each representing a unique school,
    filtered to remove the schools we don't want (while checking ceeb codes).  The original list of
    records is also filtered by side effect."""
    unique_schools = set[str]()
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
                                     'TwoOrFourYear': str(two_year(record))})
            
    return filtered_schools

# import re
# from typing import Any

# def read_canonical_name_list() -> list[dict[str,str]]:
#     """Read the canonical name list and return it."""
#     result: list[dict[str,str]] = []

#     # Do the actual reading from csv here
#     return result

# canonical_name_list: list[dict[str,str]] = read_canonical_name_list()

# def find_canonical_name(org_code: str) -> str:
#     """Using the name database, find the canonical
#     name for the school if it can be found.  If it
#     can't be found, just return the empty string."""
#     # Codes on the left should be mapped to codes on the right
#     # Some mappings are already documented in Schools_compared.csv
#     # Others you develop from schools_comparison.csv, as follows:
#     #     - Look for the schools in schools_comparison.csv that have no CEEB or MDB equivalent
#     #     - Search on the name.  If you find the name elsewhere in schools_comparison.csv,
#     #           merge the unmatched on into the matched one.
#     equivalences = {'*00016': '2519',
#                     '***022': '001311',
#                     '009917': '001311',
#                     '$00001 ': '005327'} # Just use the CEEB for name lookup
#     ceeb = ''
#     if org_code in equivalences:
#         ceeb = equivalences[org_code]
#     elif org_code.startswith('00'):
#         ceeb = org_code[-4:]
#     # If the CEEB can be found in the canonical_name_list,
#     # get the name from there
#     # Else, just return ''
#     return ''

# def fix_name(record: dict[str,str]) -> str:
#     """Fix the school name.  First, look in the
#     school name database, and get the name from there
#     if possible.  If that is not possible, apply chewing
#     gum, band-aids, and spit (the replacements heuristics)."""
#     replacements = {'C C': 'Community College',
#                     'Cmty C': 'Community College',
#                     'CC': 'Community College',
#                     'Cc': 'Community College',
#                     'Cmty Co': 'Community College',
#                     'cmty coll': 'Community College',
#                     'Col': 'College',
#                     'Coll': 'College',
#                     'Clg': 'College',
#                     'Comm': 'Community',
#                     'Cmty': 'Community',
#                     'centrl': 'Central',
#                     'I': 'Institute',
#                     'Inst': 'Institute',
#                     'Sch': 'School',
#                     'St': 'State',
#                     'TechnicalCollege': 'Technical College',
#                     'U': 'University',
#                     'Un': 'University',
#                     'Univ': 'University',
#                     # State names
#                     'Il': 'Illinois',
#                     'In': 'Indiana',
#                     'Miss': 'Mississipi',
#                     'Nc': 'North Carolina',
#                     'Nj': 'New Jersey',
#                     'Ny': 'New York',
#                     'Pa': 'Pennsylvania',
#                     'Sc': 'South Carolina',
#                     'Tx': 'Texas',
#                     'Ut': 'Utah',
#                     'Va': 'Virginia',
#                     #Acronyms
#                     'Usc': 'University of South Carolina',
#                     'Unc': 'University of North Carolina',
#                     # Random stuff
#                     'Centrl': 'Central',
#                     'Vly': 'Valley',
#                     'Intl': 'International',
#                     'Sthrn': 'Southern',
#                     'Cmps': 'Campus',
#                     'N': 'North',}

#     result = find_canonical_name(record['ORG CDE'])
#     if result == '':
#         result = record['ORG NAME'].strip()
#         # Remove strings of spaces
#         result = result.replace('  ',' ')
#         for string in replacements.keys():
#             result = re.sub(r'\b'+string+r'\b', replacements[string], result)

#     return result

# def two_year(record: dict[str,str]) -> bool:
#     """Returns True if the school in RECORD appears to be a 2-year
#     school, based on our best SWAG's applied to its name."""
#     junior = False  # Set to True if the school appears 2-year
#     return junior

# def filter_schools(transfer_credits: list[dict[str,str]]) -> list[dict[str,str]]:
#     """Takes a list of dictionaries TRANSFER_CREDITS and SAT_CREDITS, with one entry per
#     course equivalence; merges the schools in the equivalence list and 
#     returns a list of dictionaries, each representing a unique school,
#     filtered to remove the schools we don't want (while checking ceeb codes).  The original list of
#     records is also filtered by side effect."""
#     unique_schools = set()
#     filtered_schools: list[dict[str,str]] = []

#     # ID's of schools we don't want
#     bad_schools = ['**0001', '**0002', '**0003', '**0004',  '**0006',
#     #               AP        IB       'Unknown' 'Exemption' CLEP
#                    '100089', '100251', 'INTL'  ,
#     #               IB        IB        'International (Generic)'
#                    '999995']
#     #              "Comprehensive Exam"
#     merges = {'$1': '5327'} # Rewrite the OrgCode

#     for record in transfer_credits:
#         #print(record)
#         school = record['ORG CDE']
#         if school in bad_schools:
#             # Will this work?
#             del record
#             continue
#         # If this isn't a bad school
#         elif school in merges:
#             school = merges[school]
#             record['ORG CDE'] = school
#         #elif school in equivalences:
#             # Figure out how to get the name right

#         # Pad 4-digit org codes with two leading zeroes because
#         #   most of these codes appear to be 6 characters
#         if len(school) == 4 and school.isdigit():
#             school = '00' + school
#         if school not in unique_schools:
#             unique_schools.add(school)
#             filtered_schools.append({'OrgCode': school,
#                                      'College': fix_name(record),
#                                      'TwoOrFourYear': str(two_year(record))})
            
#     return filtered_schools
