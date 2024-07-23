function handleSchoolKeys(event) {
    const selectElt = event.target
    if (event.key === "ArrowDown"){
        selectElt.selectedIndex++;
        event.preventDefault();
    }
    else {
        const form = selectElt.form;
        form['CrsID'].selectedIndex = -1;
        selectElt.form.submit();
    }
}