def find_course_ID(course_list: list[dict[str, str]], orgCode: str, crsCode: str) -> str:
  course_ID = ''
  low = 0 # Bottom index still to be inspected
  high = len(course_list) # Index *after* the top index to be inspected

  while high >= low:
    mid = (high + low) // 2
    if course_list[mid]['OrgCode'] < orgCode:
      low = mid+1
    elif course_list[mid]['OrgCode'] > orgCode:
      high = mid
    # If we get here, course_list[mid]['OrgCode'] == orgCode
    elif course_list[mid]['CrsCode'] < crsCode:
      low = mid+1
    elif course_list[mid]['CrsCode'] > crsCode:
      high = mid
    else: # Found it!
      assert course_list[mid]['OrgCode'] == orgCode and course_list[mid]['CrsCode'] == crsCode
      course_ID = course_list[mid]['CrsId']
      high = low - 1

  return course_ID

def filter_equivalences(original_records: list[dict[str,str]], 
                        course_list: list[dict[str,str]]) -> list[dict[str,str]]:
  equivalences_dict = {}
  for record in original_records:
    ARC = record['ADV REQ CDE']
    if len(ARC) > 0: # Only if we have an ARC code, otherwise forget it
      orgCode = record['ORG CDE']
      crsCode = record['CRS CDE']
      key = f"{orgCode}_{crsCode}_{ARC}"
      # Iff this is the first time we've seen this course with this ARC
      if key not in equivalences_dict:
        # Find course_ID from course_list
        course_ID = find_course_ID(course_list, orgCode, crsCode)
        credit_type = record['CREDIT TYPE CDE']
        assert course_ID != '', f"Empty course_ID for {record}"
        equivalences_dict[key] = {'CrsID': course_ID, 'ARCCode': ARC,
                                  'TYear': record['TRANS YR'].strip(), 
                                  'TTerm': record['TRANS TRM '].strip(),
                                  'CreditType': credit_type}

  equivalences_list = list(equivalences_dict.values())
  return equivalences_list