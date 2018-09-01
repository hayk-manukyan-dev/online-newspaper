
function editArtcleKeywordsGet(keywords){
    CsrfToken();

    $.get('/ajax/article/keywords/edit/' + keywords, function(data){
        if (data.success == false){
            var html = '<p>'+ data.message +'</p>';
            zIndexWindow('edit_article_keywords_window', html, button = '');
        }

        else{
            html = textInputForm(value = data.keywords, id = 'edit_article_keywords', name = 'article_keywords', required = 'required', placeholder = trans('Enter keyword'), button = '', button_function = '')
            zIndexWindow('edit_article_keywords_window', html, button = '<button onclick='+'editArtcleKeywordsPost("'+ keywords +'")'+'>' + trans('Save') + '</button>');
        }
    })

}


function editArtcleKeywordsPost(keywords, success_function){
    CsrfToken();
    $.ajax({
        url : '/ajax/article/keywords/edit/' + keywords,
        type : 'POST',
        data : {'keywords' : $('#edit_article_keywords').val()},
        success : function(data){ editArtcleKeywordsPostSuccessFunction(data) },
    })
}


function editArtcleKeywordsPostSuccessFunction(data){
    if(data.success == true){
        location.reload();
    }
    else if(data.success == false){
        var html = '<p>'+ data.message +'</p>';
        zIndexWindow('edit_article_keywords_window', html, button = '');
    }
}