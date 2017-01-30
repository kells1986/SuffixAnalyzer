
function doQuery()
{
	var suffix = $("#query").val();
	$("#noresults").hide();
	$("#results").empty();
	$("#results").append("<li>Loading...</li>");
	var search = "words ending in " + suffix;
  var url = encodeURI("wolfram-query?query="+search);
  
  var jsonStream = new EventSource(url);
  jsonStream.onmessage = function (e) {
    var message = JSON.parse(e.data);
    // handle message
    $("#results").append("<li>"+message["word"] + ": " + message["definition"] + "</li>");
  };


  /*
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
        console.log(xhr);
    		$("#noresults").text("There was a problem with your query");
    		$("#noresults").show();
    		$("#results").hide();
  		}
	});
*/

}