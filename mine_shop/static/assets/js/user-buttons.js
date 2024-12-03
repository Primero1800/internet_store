
function change_add_to_cart_button(el){
    old_text = el.textContent
    el.className += ' inverse';
    el.textContent = 'Добавлено';
    setTimeout(() => {
        el.className = 'le-button';
        el.textContent = old_text;
    }, 200);
}


function click_to_tool_button(el, click_title, new_class_name, div_id, value){
    document.getElementById(div_id).setAttribute("value", value);
    old_title = el.textContent;
    el.textContent=click_title;
    old_class_name = el.className;
    el.className = new_class_name;
    setTimeout(() => {
        el.className = old_class_name;
        el.textContent = old_title;
    }, 500);
}

function get_element_value(){
    return $('#wish-compare').attr('value');
}

function get_element_value_by_id(id){
    return document.getElementById(id).getAttribute('value');
}


function cursor_pointer(el){
    el.style.cursor = 'pointer';
}