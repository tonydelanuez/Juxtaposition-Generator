var theData; 
$(document).ready(function(){
	$.get("/data", function(string) {
		theData = ' "' +  string + '" ';
	});
});

// $.getJSON('https://www.reddit.com/r/wallpapers/top/.json?count=20', function(data) 
$.getJSON("https://www.reddit.com/r/wallpaper/.json?jsonp=?", function(data) {
	console.log(data);
	var random = Math.floor(Math.random()*25);

    $.each(data.data.children, function(i,item){
    	if(i == random){
         $("<img/>").attr("src", item.data.url).appendTo("#images");
         $("<h2>").attr("id", "caption").appendTo("#images");
         $("<h3>").attr("id", "caption_name").appendTo("#images");

    	$("#caption").html(theData);
    	$("#caption_name").html("justpornhubthings");
    	}
     });
});
