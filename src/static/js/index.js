/* 

 Funzione (momentaneamente) inutilizzata. Potrebbe tornare utile in futuro ergo teniamola ancora un po'
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
    let cYear = cd.getFullYear()
    let cMonth = String(cd.getMonth() + 1)
    let cDay = String(cd.getDate()) 
    dateElement.setAttribute('max', String(cYear) + "-" + cMonth + "-" + cDay)
    dateElement.setAttribute('min', String(cYear - 10) + "-" + cMonth + "-" + cDay)
    if (isStartDate)
        dateElement.setAttribute('value', String(cYear) + "-" + cMonth + "-" + cDay)
}

initializeDate(document.getElementById("maxDate"), true);
initializeDate(document.getElementById("minDate"), false);

console.log("End of Index.js")      /* A print to see if all the index.js code ran correctly */