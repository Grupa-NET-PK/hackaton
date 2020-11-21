function runInterval(userid, url){
    var myVar = setInterval(() =>{
        console.log(userid+"");
        $.ajax({
            url: url,
            data : {
                'userid': userid
            },
            success: function (data) {
                //$("#assigned_flashcards").html("+$"+data);
                console.log(data);
            }
        })
    }, 2000);
}
