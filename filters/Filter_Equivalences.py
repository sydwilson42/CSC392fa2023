def filter_equivalences(original_records, course_list):
  equivalences_dict = {}
  for record in original_records:
    key = f"{record['org_code']}{record[coursecode']}{record['ARC']}
    if key not in equivalences_dict:
      equivalences_dict[key] = {'course_ID':'course_ID', 'ARC': record['ARC']}

  equivalences_list = []
  for key, value in equivalnces_dict.items():
      equivalnces_list.append({org_code': key.split()[0], 'course_code': key.split()[1], 'ARC': value['ARC'], 'course_ID': value['course_ID']})
