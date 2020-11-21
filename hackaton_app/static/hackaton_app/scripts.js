function runInterval(userid, url){
    var myVar = setInterval(() =>{
        $.ajax({
            url: url,
            data : {
                'userid': userid
            },
            success: function (data) {
                $("#assigned_flashcards").html(""+data);
            }
        })
    }, 500);
}

$(function(){
    $('#flashcard_anwsers[onload]').trigger('onload');
});

function runAnswersRefresh(flash_id, url){
    var myVar = setInterval(() =>{
        $.ajax({
            url: url,
            data : {
                'flash_id': flash_id
            },
            success: function (data) {
                $("#answers").html(""+data);
            }
        })
    }, 500);

}