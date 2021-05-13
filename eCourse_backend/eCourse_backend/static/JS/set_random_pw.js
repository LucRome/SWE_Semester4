const Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!$?#";
const len = 15;

function randomPw() {
    let res = [];
    for (let i = 0; i < len; i++) {
        res.push(Chars.charAt(Math.floor(Math.random() * Chars.length)));
    }
    return res.join('');
}

let pwField = document.getElementById("defaultPWField");
pwField.setAttribute("value", randomPw());