window.onload = function(){
    let change_button = document.getElementsByClassName('change')[0]

    let form = document.getElementsByClassName('change_user')[0]
    let info_block = document.getElementsByClassName('user_info_block')[0]

    change_button.addEventListener('click', function(){
        form.id = ' '
        info_block.id = 'hide'
    })
}