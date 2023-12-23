const timeElement = document.getElementById("time")
const dateElement = document.getElementById("date")

/**
* @param {Date} date 
*/
function updateClock(now) {
    const time = now.toLocaleTimeString('sv')
    const date = now.toLocaleDateString('de')

    timeElement.textContent = time
    dateElement.textContent = date
}

updateClock(new Date())
setInterval(() => {
    updateClock(new Date())
}, 1000);
