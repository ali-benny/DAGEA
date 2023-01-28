//0. Shows the spoiler containers only when all scripts are loaded.
$(document).ready(function() {
    $(".myspoiler").show();
});

//1, Hide spoiler
$( ".myspoiler span").hide();
//2, Add a button
$( ".myspoiler" ).append( "<button>La parola vincente è...</button>" );
//3, When button pressed
$( ".myspoiler button" ).click(function(){
   //3.1, Show spoiler next to the button clicked
  $( this ).prev().fadeIn(1500);
  //3.2, Hide button
  $( this ).hide();
});

//4. When the spoiler text is pressed
$( ".myspoiler span" ).click(function(){
  //4.1 Hide the spoiler text.
   $( this ).hide().fadeOut;
  //4.2 Show the button
   $( this ).next().fadeIn();
});