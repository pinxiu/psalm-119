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
function feed(user) {
    var note = document.getElementById('note').value;
    if (note)
        location.href = window.location.origin + "/feed/" + note + '/' + user;
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
function checkAns() {
    var key = document.getElementById('key').innerHTML;
    var ans = document.getElementById('ans').value;
    if (ans != key.substring(0, ans.length)) {
        document.getElementById('mark').innerHTML = '&#10008';
    } else if (ans.length == key.length) {
        document.getElementById('mark').innerHTML = '&#10004';
    } else {
        document.getElementById('mark').innerHTML = '&#9997';
    }
}

function showAns() {
    if (document.getElementById('showAns').value == 'Show Answer') {
        document.getElementById('showAns').value = 'Hide Answer';
        document.getElementById('key').style = "width:500px; visibility:visible";
    } else {
        document.getElementById('showAns').value = 'Show Answer';
        document.getElementById('key').style = "width:500px; visibility:hidden";
    }
}

function setHeight(field){
  document.getElementById(field).style.height = "106px";
  document.getElementById(field).style.height = (document.getElementById(field).scrollHeight)+'px';
}