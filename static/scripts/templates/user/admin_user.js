function getUser(add_in){
    CsrfToken()
    var html = ''
    $.get('/json/admin/getusers/', function(user){

        for(index = 0; index < Object.keys(user).length; index++){
            html += '<div class="card" style="width: 18rem;"><img class="card-img-top" src="'+user[index].fields.avatar+'" alt="Card image cap"><div class="card-body"><h5 class="card-title">'+user[index].fields.first_name + ' ' + user[index].fields.last_name + '</h5>';

            for(group_index = 0; group_index < Object.keys(user[index].fields.groups).length; group_index++){
                html += '<p class="card-text">'+ user[index].fields.groups[group_index].name + '<a href="/group/removeuser/'+ user[index].pk+'/'+user[index].fields.groups[group_index].pk+'">x</a></p>';
            }

            html += '</div></div>';

        }

    $(add_in).append(html)

    })

}


function userCardStabilizate(){

}




