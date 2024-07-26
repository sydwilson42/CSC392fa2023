function initializeForm(start_focus, other_data) {
    console.log('other_data', other_data);
    // Set event listeners for the schools dropdown
    const schoolsDropdown = document.getElementById('OrgCode');
    schoolsDropdown.addEventListener('keydown', handleSchoolKeys);
    schoolsDropdown.addEventListener('change', handleSchoolChange);

    // Enable the Find Equivalences button iff the course dropdown has a selection
    document.getElementById('CrsID').addEventListener('change', 
        (event) => document.getElementById('bttn_eq').disabled = (event.target.selectedIndex <= 0));

    // If start_focus is specified, set the focus in the correct place.  This doesn't always work as expected.
    //console.log("start_focus", start_focus);
    if (start_focus) {
        const elt = document.getElementById(start_focus);
        if (elt) {
            elt.focus({focusVisible: true});
        }
        else {
            console.log('Cannot focus nonexistent element', start_focus);
        }
        
    }
}

function handleSchoolKeys(event) {
    const selectElt = event.target;
    selectElt.form['CrsID'].selectedIndex = 0;
    switch (event.key) {
        case "ArrowDown":
        case "ArrowRight":
            selectElt.selectedIndex++;
            event.preventDefault();
            break;
        case "ArrowUp":
        case "ArrowLeft":
            selectElt.selectedIndex--;
            event.preventDefault();
            break;
        // Special processing for Tab because of its navigation use
        case "Tab":
            const startFocusElt = document.getElementById('start_focus');
            if (event.shiftKey) {
                startFocusElt.value = "OrgCode"; // Probably the wrong choice
            }
            else {
                startFocusElt.value = "CrsID";
            }
            // Note fall-through!
        case "Enter":
        case " ":
        case "Accept":
        case "Execute":
        case "Finish":
        case "Select":
            selectElt.form.submit();
            break;
    }
}

function handleSchoolChange(event) {
    const formElt = event.target.form;
    formElt['CrsID'].selectedIndex = 0;
    formElt.submit();
}