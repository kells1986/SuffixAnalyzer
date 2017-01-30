
function doQuery()
{
	var suffix = $("#query").val();
	$("#noresults").hide();
	$("#results").empty();
	$("#results").append("<li>Loading...</li>");
	var search = "words ending in " + suffix;

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
    			for (var result=0; result < response.length; result++)
    			{
    			 $("#results").append("<li>"+response[result]["word"] + ": " + response[result]["definition"] + "</li>");	
    			}
    		}
    			
  		},
  		error: function(xhr) {
    		$("#noresults").text("There was a problem with your query");
    		$("#noresults").show();
    		$("#results").hide();
  		}
	});

}