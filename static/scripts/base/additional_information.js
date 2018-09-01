function getCurrentLanguage(){
    return $('#language_code').text()
}


function getZIndex(){
    return $('#current_z_index').text()
}

function increaseZIndex(){
    var z_index = getZIndex();
    $('#current_z_index').text(parseInt(z_index) + 1)
}

function decreaseZIndex(){
    var z_index = getZIndex();
    $('#current_z_index').text(parseInt(z_index) - 1)
}