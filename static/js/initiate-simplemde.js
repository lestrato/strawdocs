
function create_simplemde(element) {
  return new SimpleMDE ({
   element: document.getElementById(element),
   spellChecker: false,
   status: false,
   renderingConfig: {
       singleLineBreaks: true,
   },
   previewRender: function(plainText, preview) { // Async method
       setTimeout(function(){
           preview.innerHTML = customMarkdownParser(plainText);
       }, 250);

       return "Loading...";
   },
   });
}

function customMarkdownParser(plainText) {
  return md.render(plainText);
}
