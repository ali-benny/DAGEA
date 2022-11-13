let searchBy = (searchCase) => {
    var optionsButton = document.getElementById("tweetSearchBarButton")
    switch (searchCase) {
        case 0:
            optionsButton.innerHTML = "Research by user"
            break;
        case 1:
            optionsButton.innerHTML = "Research by tag"
            break;
        default:
            break;
    }
}
