function resetDates(whichDate) {
	var currentDate = new Date()
	var resettedDate = new Date()

	if (whichDate === 'maxDate') {
		resettedDate.setMinutes(currentDate.getMinutes() - 1)
		resettedDate = resettedDate.toISOString().substring(0,16)
	}
	else if (whichDate === 'minDate') {
		resettedDate.setDate(currentDate.getDate() - 7)
		resettedDate.setMinutes(resettedDate.getMinutes() + 1)
		resettedDate = resettedDate.toISOString().substring(0,16)
	}
	document.getElementById(whichDate).value = resettedDate
}