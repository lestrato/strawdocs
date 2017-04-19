
function create_simplemde(element) {
  return new SimpleMDE ({
   element: document.getElementById(element),
   spellChecker: false,
   status: false,
   renderingConfig: {
       singleLineBreaks: true,
   },
   });
}