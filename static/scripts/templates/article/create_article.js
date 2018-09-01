/*
Required
choiceForm() from base.HTMLTagsBootstrapAdapted
*/


function createArticeKeywordsForm(){
    /* with article keywords input field add categories choice field */

    var input_keywords = textInputForm(value = '', id = 'keywords_field', name = 'keywords', required = 'requeired', placeholder = trans('Please Enter keywords of article'))

    zIndexWindow('create_article_window', input_keywords, button = '<button onclick="continueCreateKeywords()">' + trans('Continue') + '</button>');
}


function continueCreateKeywords(){
    CsrfToken()
    $.ajax({
        url : '/ajax/article/keywords/create/',
        type : 'POST',
        data : {'keywords' : $('#keywords_field').val()},
        success : function(data){
            console.log(data)
        }
    })
}

