function search() {
    var reference = document.getElementById('reference').value;
    var number = document.getElementById('number');
    if (number == null || number.value == 'Show Verse Number')
    	location.href = window.location.origin + "/search/" + reference + '/false';
    else
    	location.href = window.location.origin + "/search/" + reference + '/true';
}
function submit(reference) {
    var note = document.getElementById('note').value;
    var flag;
    if (number == null || number.value == 'Show Verse Number')
    	flag = 'false';
   	else
   		flag = 'true';
    if (reference && note)
	    location.href = window.location.origin + "/submit/" + reference + '/' + note + '/' + flag;
}
function check(reference) {
    if (reference)
	    location.href = window.location.origin + "/check/" + reference;
}
function store(reference) {
    var flag;
    if (number == null || number.value == 'Show Verse Number')
        flag = 'false';
    else
        flag = 'true';
    if (reference)
        location.href = window.location.origin + "/store/" + reference+ '/' + flag;
}
function change(reference) {
	if (document.getElementById('number').value == 'Show Verse Number') {
		document.getElementById('number').value = 'Hide Verse Number';
		location.href = window.location.origin + "/search/" + reference + '/true';
	} else {
		document.getElementById('number').value = 'Show Verse Number';
		location.href = window.location.origin + "/search/" + reference + '/false';
	}
}