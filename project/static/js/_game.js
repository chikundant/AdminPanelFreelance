window.onload = function(){
    edit_button = document.getElementsByClassName('edit_button')

    var step;
    for (step = 0; step < edit_button.length; step++) {

        edit_button[step].addEventListener('click', function(event){
            let target = event.target
            target.closest('.game').childNodes[1].id = 'hide'        
            target.closest('.game').childNodes[3].id = 'show'
            target.closest('.game').childNodes[5].id = 'hide'
        })

    }

}