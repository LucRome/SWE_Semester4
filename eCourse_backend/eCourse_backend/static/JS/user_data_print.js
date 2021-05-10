// print the content of the user information table
function userInfoPrint()
{
    let divToPrint = document.getElementById('user_information');
    let newWin = window.top.open();
    newWin.document.open();
    newWin.document.write('\
        <html>\
        <head>\
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">\
        </head>\
        <body onload="window.print()">' 
            + divToPrint.innerHTML +
        '</body></html>');
    newWin.document.close();

    setTimeout(function(){newWin.close();}, 10);
}

userInfoPrint();