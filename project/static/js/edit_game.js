window.onload = function(){

    let edit_field_area = document.getElementsByClassName('edit_field_area')
    
    for (let i = 0; i < edit_field_area.length; i+= 1){
        tmp = edit_field_area[i].innerHTML
        tmp = tmp.replace(new RegExp('&lt;', 'g'), '<');
        tmp = tmp.replace(new RegExp('&gt;', 'g'), '>');
        tmp = tmp.replace(new RegExp('<br>', 'g'), '\r\n');
        edit_field_area[i].innerHTML = tmp
    }
    

}