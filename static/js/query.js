
function doQuery()
{
	var suffix = $("#query").val();
	$("#noresults").hide();
	$("#results").empty();
	$("#results").append("<li id='loading'>Loading...</li>");
	
  var search = "words ending in " + suffix;
  var url = encodeURI("wolfram-query?query="+search);
  
  var wolframStream = new EventSource(url);
  
  wolframStream.onmessage = function (e) {
    $("#loading").hide();
    var rawString = e.data;
    var parsedString = rawString.split(":::");
    $("#results").append("<li>"+parsedString[0] + ": " + parsedString[1] + "</li>");
  };

  wolframStream.onerror = function(e) {
    wolframStream.close();
  };


}