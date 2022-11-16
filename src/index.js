var cd = new Date();        /* cd stay for Current Date */

let searchBy = (searchCase) => {
    var optionsButton = document.getElementById("tweetDrp")
    switch (searchCase) {
        case 0:
            optionsButton.innerHTML = "Research by username "
            break;
        case 1:
            optionsButton.innerHTML = "Research by keyword & hashtag "
            break;
        default:
            break;
    }
}

let initializeDate = (dateElement, isStartDate) => {
    var cYear = cd.getFullYear()
    var cMonth = String(cd.getMonth() + 1)
    var cDay = String(cd.getDate()) 
    dateElement.setAttribute('max', String(cYear) + "-" + cMonth + "-" + cDay)
    dateElement.setAttribute('min', String(cYear - 10) + "-" + cMonth + "-" + cDay)
    if (isStartDate)
        dateElement.setAttribute('value', String(cYear) + "-" + cMonth + "-" + cDay)
}

initializeDate(document.getElementById("startDate"), true);
initializeDate(document.getElementById("limitDate"), false);

console.log("End of Index.js")