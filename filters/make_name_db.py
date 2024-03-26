from read_write_csv import read_from_csv, write_csv
import re

def make_master_schools_list(CEEB_list: list[dict[str, str]], 
                          nursing_list: list[dict[str,str]]) -> list[dict[str,str]]:
    """Create a single master school name list from the CEEB list
    and the NursingCAS list."""
    CEEB_list.sort(key=lambda school: school['CEEB'])
    #print(CEEB_list[:100])
    nursing_list = list(filter(lambda school: school['ceeb_code'].isdigit(), 
                               nursing_list))
    nursing_list.sort(key=lambda school: school['ceeb_code'])
    print(len(nursing_list))
    #print(nursing_list[:100])
    CEEB_copy_fields = ('Name', 'State', 'Country')
    nursing_copy_fields = ('name', 'mdb_code', 'state', 'country',
                           'fice_code', 'ipeds_code', 
                           'accreditation_agency')

    schools: list[dict[str, str]] = []
    ceeb_i = 0
    nursing_i = 0
    while ceeb_i < len(CEEB_list) or nursing_i < len(nursing_list):
        school: dict[str, str] = {}
        # Set the current CEEB number
        current_ceeb = ''
        if (nursing_i >= len(nursing_list)):
            current_ceeb = CEEB_list[ceeb_i]['CEEB']
        elif (ceeb_i >= len(CEEB_list)):
            current_ceeb = nursing_list[nursing_i]['ceeb_code']
        else:
            current_ceeb = min(CEEB_list[ceeb_i]['CEEB'], 
                               nursing_list[nursing_i]['ceeb_code'])
        assert current_ceeb.isdigit()

        school['CEEB'] = current_ceeb
        # If this CEEB matches the current CEEB in the CEEB_list, copy that data
        if (ceeb_i < len(CEEB_list)) and \
            (current_ceeb == CEEB_list[ceeb_i]['CEEB']):
            for field in CEEB_copy_fields:
                school['CEEB_'+field] = CEEB_list[ceeb_i][field]
            ceeb_i = ceeb_i + 1
        else: # All the records need to have the same fields, even if they're empty
            for field in CEEB_copy_fields:
                school['CEEB_'+field] = ''
        # If this CEEB matches the current CEEB in the nursing_list, copy that data
        if (nursing_i < len(nursing_list)) \
            and (current_ceeb == nursing_list[nursing_i]['ceeb_code']):
            for field in nursing_copy_fields:
                school['nursing_'+field] = nursing_list[nursing_i][field]
            nursing_i = nursing_i + 1
        else: # Put in placeholders for the nursing fields
            for field in nursing_copy_fields:
                school['nursing_'+field] = ''
        
        # Fix the case in the nursing_name
        school['nursing_name'] = school['nursing_name'].title()
        # Put back state abbreviations, if they're in the name
        state = school['nursing_state']
        if state.title() in school['nursing_name']:
            school['nursing_name'] = \
                re.sub(r'\b'+state.title()+r'\b', state, school['nursing_name'])

        schools.append(school)

    print(len(schools))
    return schools

def make_comparison_list(transfer_schools_list: list[dict[str,str]],
                         schools_list: list[dict[str,str]]) -> list[dict[str,str]]:
    transfer_schools_list.sort(key=lambda school: school['OrgCode'])
    schools_list.sort(key=lambda school: school['CEEB'])
    comparison_list: list[dict[str,str]] = []

    i = 0
    for x_school in transfer_schools_list:
        record: dict[str,str] = {}
        for field in x_school.keys():
            record[field] = x_school[field]
        orgcode = x_school['OrgCode']
        # Provide default, in case there's no match
        for field in schools_list[0].keys():
            record[field] = ''

        ceeb = ''
        if orgcode.startswith('00'):
            ceeb = orgcode[2:]
            # record['CEEB'] = ceeb
            while (i < len(schools_list)) and \
                  (schools_list[i]['CEEB'] < ceeb):
                i = i + 1
            if (i < len(schools_list)) and \
                (schools_list[i]['CEEB'] == ceeb):
                for field in schools_list[i].keys():
                    record[field] = schools_list[i][field]
        comparison_list.append(record)
    return comparison_list

def main(args: list[str]) -> int:
    CEEB_list: list[dict[str, str]] = read_from_csv('sat-score-reporting-code-list-working.csv')
    print(len(CEEB_list))
    nursing_list: list[dict[str,str]] = read_from_csv('Master College Code List 20240314.csv')
    print(len(nursing_list))

    schools_list = make_master_schools_list(CEEB_list, nursing_list)
    write_csv('school_names.csv', schools_list)

    transfer_schools_list: list[dict[str, str]] = read_from_csv('Schools.csv')
    comparison_list = make_comparison_list(transfer_schools_list, schools_list)
    write_csv('schools_comparison.csv', comparison_list)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
