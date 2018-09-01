function editEmail(){
    CsrfToken()
    var email = $('input[name="email"]').val();
    $.ajax({
        type:"POST",
        url:"/ajax/editemail",
        data:{"email" : email},
        success:function(data){
            if(data.response == "success"){
                alert(data.response);
            }
            else if(data = '0'){
                alert('skip')
            }
            else{
                alert(data.message)
            }
        }
    })
}



function editFirstName(){
    CsrfToken()
    var first_name = $('input[name="first_name"]').val();
    $.ajax({
        type:"POST",
        url:"/ajax/editfirstname",
        data:{"first_name" : first_name},
        success:function(data){
            if(data.response == "success"){
                alert(data.response);
            }
            else{
                alert(data.message)
            }
        }
    })
}



function editLastName(){
    CsrfToken()
    var last_name = $('input[name="last_name"]').val();
    $.ajax({
        type:"POST",
        url:"/ajax/editlastname",
        data:{"last_name" : last_name},
        success:function(data){
            if(data.response == "success"){
                alert(data.response);
            }
            else{
                alert(data.message);
            }
        }
    })
}


function editAvatarForm(){
    var id = 'editAvatarForm';
    $.get( "/avataredit", function( data ) {
        $.when($('body').append("<div id="+id+">" + data + "</div>")).then($('#'+id + ' button').hide());
    })
}


function editAvatarPost(){
    $('#id_avatar').on('change', function(){
        var $input = $('#id_avatar');
        var fd = new FormData;
        fd.append('avatar', $input.prop('files')[0]);
        CsrfToken()
        $.ajax({
            type : 'POST',
            url : 'ajax/editavatar',
            data : fd,
            processData: false,
            contentType: false,
            success : function(data){
                alert(data.response)
                $(location).attr("href", window.location.href)
            }
        })

    })
}
