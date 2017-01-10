$(document).ready(function(){

  $(document).on("click", ".btn-add", function(e){
    e.preventDefault();
    count=Number($('#id_option_count').val());
    var tocopy=$(this).parents(".form-group");
    var current=$(tocopy).parents(".input-group");
    var newEntry=$(tocopy).clone().appendTo(current);
    newEntry.find('input').attr("id", "id_option_"+count).attr("name", "option_"+count).attr('placeholder', "Option "+String(Number(count)+1));

  count+=1;
  $('#id_option_count').val(count);
});

});
