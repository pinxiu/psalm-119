function search(user) {
    var reference = document.getElementById('reference').value;
    if (reference) {
        var number = document.getElementById('number');
        if (number == null || number.value == 'Show Verse Number')
        	location.href = window.location.origin + "/search/" + reference + '/false/' + user;
        else
        	location.href = window.location.origin + "/search/" + reference + '/true/' + user;
    }
}
function submit(reference, user) {
    var note = document.getElementById('note').value;
    if (note)
        note = note.replace(/(?:\r\n|\r|\n)/g, '<br>');
    var flag;
    if (number == null || number.value == 'Show Verse Number')
    	flag = 'false';
   	else
   		flag = 'true';
    if (reference && note)
	    location.href = window.location.origin + "/submit/" + reference + '/' + note + '/' + flag + '/' + user;
}
function check(reference, user) {
    if (reference)
	    location.href = window.location.origin + "/check/" + reference + '/' + user;
}
function store(reference, user) {
    var flag;
    if (number == null || number.value == 'Show Verse Number')
        flag = 'false';
    else
        flag = 'true';
    if (reference)
        location.href = window.location.origin + "/store/" + reference+ '/' + flag + '/' + user;
}
function change(reference, user) {
	if (document.getElementById('number').value == 'Show Verse Number') {
		document.getElementById('number').value = 'Hide Verse Number';
		location.href = window.location.origin + "/search/" + reference + '/true/' + user;
	} else {
		document.getElementById('number').value = 'Show Verse Number';
		location.href = window.location.origin + "/search/" + reference + '/false/' + user;
	}
}