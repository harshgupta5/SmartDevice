$(document).ready(function () {
  $.getJSON("/fetchstates",function(data){
      //alert(data)
      $.each(data,function(index,item){
      $('#state').append($('<option>').text(item[1]).val(item[0]))
      })

   })

 $('#state').change(function(){

  $.getJSON("/fetchcities",{stateid:$('#state').val()},function(data){
      $('#city').empty()
      $('#city').append($('<option>').text("-City-"))
   $.each(data,function (index,item) {
   $('#city').append($('<option>').text(item[2]).val(item[0]))
   })
  })
})
})


