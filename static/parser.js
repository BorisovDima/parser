$(document).on('click', '[data-id="parse-articles"]', function(){
    $('[data-id="articles"]').html('')
    $('[data-id="loading"]').show()
    $.ajax({
          url: '/',
          method: 'POST',
          success: function(json){
            $('[data-id="loading"]').hide()
            $('[data-id="articles"]').html(json['data'])
          },
          error: function(data) {
              $('[data-id="articles"]').html('<h1> Something was wrong...' +
              '<button class="btn btn-danger" data-id="parse-articles"> Try again </button> </h1> ')
           },
    })


})


