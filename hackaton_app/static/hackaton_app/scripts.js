//setInterval(check_assigned_flashcards, 2000);
//
//function check_assigned_flashcards(userid){
//    console.log(userid);
//    $.ajax({
//        url: 'check_assigned_flashcards/',
//        data : {
//            'userid': userid
//        },
//        success: function (data) {
//            $("#assigned_flashcards").html("+$"+data);
//        }
//    })
//};