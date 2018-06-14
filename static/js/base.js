function search() {
    var reference = document.getElementById('reference').value;
    location.href = window.location.origin + "/search/" + reference;
}
function submit(reference) {
    var note = document.getElementById('note').value;
    location.href = window.location.origin + "/submit/" + reference + '/' + note;
}