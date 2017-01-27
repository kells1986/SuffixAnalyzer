
function do_query()
{
	$.ajax({
  		url: "wolfram-query",
  		type: "get", //send it through get method
  		data: { 
    		query: "words ending in lly"
  		},
  		success: function(response) {
    		//Do Something
    		$("#noresults").hide();
    		$("#results").empty();
    		for (var i=0; i < response.length; i++)
    		{
    			$("#results").append("<li>"+response[i]+"</li>");	
    		}	
    		console.log("Done");
  		},
  		error: function(xhr) {
    		//Do Something to handle error
    		$("#noresults").text("There was a problem with your query");
    		$("#noresults").show();
    		$("#results").hide();
  		}
	});

}