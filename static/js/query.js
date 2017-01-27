
function do_query()
{
	var suffix = $("#query").val();
	console.log(suffix);
	$("#noresults").hide();
	$("#results").empty();
	$("#results").append("<li>Loading...</li>");
	search = "words ending in " + suffix;

	$.ajax({
  		url: "wolfram-query",
  		type: "get", //send it through get method
  		data: { 
    		query: search
  		},
  		success: function(response) {
    		$("#results").empty();
    		if (response.length == 0)
    		{
    			$("#results").append("<li>There were no results for the suffix: " + suffix + "</li>");
    		}
    		else
    		{
    			for (var i=0; i < response.length; i++)
    			{
    			$("#results").append("<li>"+response[i]["word"] + ": " + response[i]["definition"] + "</li>");	
    			}
    		}
    			
    		console.log("Done");
  		},
  		error: function(xhr) {
    		$("#noresults").text("There was a problem with your query");
    		$("#noresults").show();
    		$("#results").hide();
  		}
	});

}