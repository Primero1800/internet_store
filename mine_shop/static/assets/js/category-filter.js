function get_filter_statuses(n) {
    const result = new Array();
    result.push(n)
    for (let i = 0; i < n; i++) {
        var checkBox = document.getElementById("brand" + i);
        if (checkBox.checked == true){
            result.push(true);
        }else{
            result.push(false);
        }
    }
    var select = document.getElementById("ordering-sort")
    result.push(select.value)

    var select = document.getElementById("paging-count")
    result.push(select.value)

    var className = $('#grid-view').attr('class');
    result.push(className)

    return result
}



function get_current_page() {
    return $('#div_category_grid').attr('class');
}

