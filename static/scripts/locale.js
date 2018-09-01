/*
Required additional_information (getCurrentLanguage)

*/

function en(){
    return {
        'Save' : 'Save',
        'Delete' : 'Delete',
        'Choose a category' : 'Choose a category',
        'Something went wrong' : 'Something went wrong',
    }
}


function ru(){
    return {
        'Save' : 'Сохранить',
        'Delete' : 'Удалить',
        'Choose a category' : 'Выбирайте категорию'
    }
}


function getTranslated(text, language){
    if(language == 'en'){
        translated = en()[text];
    }
    else if(language == 'ru'){
        translated = ru()[text];
    }
    else{
        translated = text;
    }


    if(typeof translated == 'undefined'){
        return text
    }
    else{
        return translated
    }

}


function trans(text){
    /* If function can't find required language tranlated text then it will return entered text */

    language = getCurrentLanguage();

    return getTranslated(text, language)
}