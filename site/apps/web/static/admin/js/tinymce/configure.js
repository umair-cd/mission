/**
 * Created by jose on 11/2/17.
 */

if(!$){
  $ = django.jQuery;
}


$(function () {
    tinymce.init({
        selector: "textarea.vLargeTextField",
        language: "en",
        skin: "lightgray",
        statusbar: false,
        toolbar: 'undo redo formatselect bold italic alignleft aligncenter alignright bullist numlist outdent indent code',
        theme: 'modern',
        height: 300,
        plugins: [
            'advlist autolink link lists charmap print preview hr spellchecker',
            'searchreplace wordcount visualblocks visualchars fullscreen insertdatetime nonbreaking',
            'save table contextmenu directionality paste textcolor wordcount'
        ],
    });
});
