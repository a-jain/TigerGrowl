function onTextSelected() {
	var option = $('option:selected', this); 
	var name = option.text();
	var url = option.val();
	
	$('#selectionTitle').text(name);
	$('#spritzer2').data('controller').setUrl(url);
}

$(document).ready(function() {
	// Add selection handler
	$("#textList").on("change", onTextSelected);  
});