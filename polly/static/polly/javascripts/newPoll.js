$(document).ready(function(){
numoption=2;

  $(document).on("click", ".btn-remove", function(e){
    e.preventDefault();
    var toremove=$(this).parents(".form-group");
    $(toremove).remove();
    count=Number($('#id_option_count').val());
    count-=1;
    $('#id_option_count').val(count);
  })

  $(document).on("click", ".btn-add", function(e){
    e.preventDefault();
    count=Number($('#id_option_count').val());
    numoption+=1
    var tocopy=$(this).parents(".form-group");
    var current=$(tocopy).parents(".input-group");
    var newEntry=$(tocopy).clone().appendTo(current);
    newEntry.find('input').attr("id", "id_option_"+String(numoption-1)).attr("name", "option_"+String(numoption-1)).attr('placeholder', "Option "+String(numoption));

    $(this).removeClass("btn-add").addClass("btn-remove")
    $(this)[0].innerHTML="-"
    console.log($(this)[0].innerHTML)


  count+=1;
  $('#id_option_count').val(count);
});

});
