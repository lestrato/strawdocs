tinymce.init({
  selector: 'textarea',
  height: 100,
  theme: 'modern',
  removed_menuitems: 'newdocument',
  plugins: [
    'advlist autolink lists link image charmap preview hr',
    'searchreplace code eqneditor',
    'insertdatetime save table directionality',
    'paste textpattern imagetools'
  ],
  toolbar1: 'bold italic | alignleft aligncenter alignright alignjustify | bullist numlist | outdent indent | link image eqneditor',
});
