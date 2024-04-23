def filter_arcs(transfer_credits: list[dict[str,str]]) -> list[dict[str,str]]:
    """Takes a list of dictionaries TRANSFER_CREDITS, with one entry
    per course equivalence.  Any merging of schools is assumed to have
    happened already. Any merging of courses is assumed to have
    happened already. This function merges duplicate ARCs and
    filters out bad ARCs in TRANSFER_CREDITS by side effect.  This
    function returns a list of dictionaries representing the data for
    the ARCs table in the database."""


    unique_ARCs: list[dict[str, str]] = []
    for record in transfer_credits:
        ARC_code = record['ADV REQ CDE']
        credit_type = record['CREDIT TYPE CDE']
        # See if the ARC Code is empty, then try to find the ARC Code.
        #if ARC_code == '':
            # Unsure what to put here.
        if credit_type == 'TR':
            if ARC_code not in unique_ARCs:
                unique_ARCs.append({'ARCCode' : ARC_code, 
                                    'CreditType': credit_type})
    return unique_ARCs
