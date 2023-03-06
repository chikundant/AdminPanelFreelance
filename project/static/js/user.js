window.onload = function(){
    let change_button = document.getElementsByClassName('change')[0]

    let form = document.getElementsByClassName('change_user')[0]
    let info_block = document.getElementsByClassName('user_info_block')[0]

    let dec = document.getElementsByClassName('dec')

    change_button.addEventListener('click', function(){
        form.id = ' '
        info_block.id = 'hide'
    })

    for (let i = 0; i < dec.length; i+= 1){
        tmp = dec[i].innerHTML
        tmp = tmp.replace(new RegExp('&lt;', 'g'), '<');
        tmp = tmp.replace(new RegExp('&gt;', 'g'), '>');
        dec[i].innerHTML = tmp
    }

}