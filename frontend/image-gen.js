$(document).ready(function(){
	$.get("/get-comment", function(comment) {
		return ` "${comment.comment}" `;
	}).then((comment) => {
	    $("<img>").attr("src", "/get-image").appendTo("#images");
	    $("<h2>").attr("id", "caption").appendTo("#images");
	    $("<h3>").attr("id", "caption_name").appendTo("#images");
	    $("#caption").text(comment);
	    $("#caption_name").text("justpornhubthings");
	})
});
