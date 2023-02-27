window.onload = function(){
    let search_window_button = document.getElementsByClassName('search_window_button')[0]
    let add_window_button = document.getElementsByClassName('add_window_button')[0]

    let search_block = document.getElementsByClassName('search_block')[0]
    let add_user_block = document.getElementsByClassName('add_user_block')[0]


    search_window_button.addEventListener('click', function(){
        add_user_block.id = 'hide'
        search_block.id = ''

        search_window_button.id = 'pressed'
        add_window_button.id = 'unpressed'

    })

    add_window_button.addEventListener('click', function(){
        add_user_block.id = ''
        search_block.id = 'hide'

        search_window_button.id = 'unpressed'
        add_window_button.id = 'pressed'
    })
}
