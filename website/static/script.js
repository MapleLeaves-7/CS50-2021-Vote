
function isNumberKey(evt) {
    // Get the Unicode of the character of the key pressed into the textbox (that triggered the event)
    // If the browser surpports event.which, use that.
    // If not, use event.keyCode to get the Unicode
    var char_unicode = evt.which || event.keyCode

    // If the character entered is not within 0 to 9
    if (char_unicode > 31 && (char_unicode < 48 || char_unicode > 57)) {

        document.getElementById("paragraph").innerHTML = "Please enter only positive integer numbers"
        // Do not allow user to enter it into the textbox
        return false;
    }

    document.getElementById("paragraph").innerHTML = ""
    return true;
}
