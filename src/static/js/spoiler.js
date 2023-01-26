//0. Shows the spoiler containers only when all scripts are loaded.
$( 'eredita.html' ).ready(function() {
    $(".spoiler").show();
});

//1, Hide spoiler
$( ".spoiler span").hide();
//2, Add a button
$( ".spoiler" ).append( "<button>La parola vincente è...</button>" );
//3, When button pressed
$( "button" ).click(function(){
   //3.1, Show spoiler next to the button clicked
  $( this ).prev().fadeIn(1500);
  //3.2, Hide button
  $( this ).hide();
});

//4. When the spoiler text is pressed
$( "span" ).click(function(){
  //4.1 Hide the spoiler text.
   $( this ).hide().fadeOut;
  //4.2 Show the button
   $( this ).next().fadeIn();
});