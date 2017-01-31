function removeRequired() {
 /* Remove the 'required' field for the hidden input textarea
  * not doing so will pick up an unavoidable error for validating the textarea
  */
  $("textarea").removeAttr("required");
}
