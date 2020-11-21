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
    }, 2000);
}
