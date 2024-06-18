$(function(){
  $(window).on('load',function(){
      $('.loader').delay(500).fadeOut(500);
      $('.loader-bg').delay(800).fadeOut(700);
  });
  setTimeout(function(){
      $('.loader-bg').fadeOut(500);
  },5000);
});

