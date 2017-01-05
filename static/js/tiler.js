

$('#picker').colpick({
  layout:'rgb',
  submit:0,
  colorScheme:'dark',
  onChange:function(hsb,hex,rgb,el,bySetColor) {
    $(el).css('border-color','#'+hex);
    var led_number = document.getElementById('led_number').value;
    console.log(led_number);
    $.get( "http://10.0.1.18/color?red="+rgb.r+"&green="+rgb.g+"&blue="+rgb.b+"&position="+led_number);

    // Fill the text box just if the color was set using the picker, and not the colpickSetColor function.
    if(!bySetColor) $(el).val(hex);
  }
}).keyup(function(){
  $(this).colpickSetColor(this.value);
});
function power(){
  $.get( "http://10.0.1.18/power");
}
