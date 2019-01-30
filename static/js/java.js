$(document).ready(function(){
    document.getElementById("searchgifs").addEventListener("click", getData);
});

function getData(){
    var input = document.getElementById("searchtext").value;


    var xhr = $.get("https://api.giphy.com/v1/gifs/search?q="+input+"&api_key=bJIEppj9qn0rqQZuSQKrgu0gC6iuqyhO&limit=8");
    xhr.done(function(response)
        { console.log("success got data", response);

        var respond = response.data

        $('.inner').html('');

        for (i in respond)
        {
            $('.inner').append("<img src= '"+respond[i].images.original.url+"' style='height: 200px; width: 200px;'/>")

            }
                    });
}