/* Bootstrap 4.1
   required locale.js
*/

function textInputForm(value = '', id = '', name = '', required = '', placeholder = '', button = '', button_function = ''){

  /*
  EXAMPLE
        $('body').append(textInputForm(value = 'some_value', id = '#name_id', name = 'name', required = 'required', placeholder = 'input name', button = 'save' button_function = 'ajax_save()'))
  */

  var html = '<div class="input-group mb-3"><input type="text" id="'+id+'" name="'+name+'" class="formcontrol" value="'+value+'" placeholder="'+placeholder+'" '+required+'>';

  if(button != ''){
    html += '<div class="input-group-append"><button class="btn btn-outline-secondary" type="button" onclick="'+button_function+'">'+button+'</button></div>'
  }

  html += '</div>'

  return html
}



function choiceForm(choicedict, empty = '', button = '', button_function = '', div_id = '', select_id = ''){

  /*
  EXAMPLE
  $('body').append(choiceField({0:{"name":'valod', "value":'1'}, 1:{"name":'ashot', "value":'2'}}, 'choice...', button='hello', button_function = 'none', div_id = 'new', select_id = 'selectnew'))
   */

  var html = '<div id="'+div_id+'" class="input-group"><select id="'+select_id+'" class="custom-select"><option selected>'+empty+'</option>';

  var option = '';
  for(i = 0; i < Object.keys(choicedict).length; i++){
    option += '<option value="'+choicedict[i].value+'">'+choicedict[i].name+'</option>'
    }

  html += option;
  html += '</select>'

  if (button != ''){
    html += '<div class="input-group-append"><button onclick="'+button_function+'" class="btn btn-outline-secondary" type="button">'+button+'</button></div>';
  }

  html += '</div>'
  return html
}


function closeZIndexWindow(id){
    $(id).remove();
    decreaseZIndex();
}

function zIndexWindow(window_id, inside_html, button){
    increaseZIndex()
    var html = '<di id="'+window_id+'"  class="container">';
    html += inside_html;

    if (button != ''){
        html += button;
    }

    html += '<button onclick="closeZIndexWindow('+window_id+')">' + trans('Close') + '</button>'
    html += '</div>';
    $('body').append(html);
}

