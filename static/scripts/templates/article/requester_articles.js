function removeInitialArticle(keywords){
    CsrfToken();
    $.ajax({
        url : '/ajax/article/remove/initialarticle/' + keywords,
        type : 'POST',
        data : {},
        success : function(data){
            if(data.success == true){
                $('#initialarticle-' + keywords).remove();
            }
            else if(data.success == false){
                alert(data.message)
            }
            else{
                alert(trans('Something went wrong'))
            }
        }
    })
}



function removeArticle(article_pk){
    CsrfToken();
    $.ajax({
        url : '/ajax/article/remove/article/' + article_pk,
        type : 'POST',
        data : {},
        success : function(data){
            if(data.success == true){
                $('#article-' + article_pk).remove()
            }
            else if(data.success == false){
                alert(data.message)
            }
            else{
                alert(trans('Something went wrong'))
            }
        }
    })
}