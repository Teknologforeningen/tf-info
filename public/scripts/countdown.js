const MS_TO_SECONDS = 1000;
const MS_TO_MINUTES = 60000;
const MS_TO_HOURS = 3600000;
const MS_TO_DAYS = 86400000;

/**
 * @param {Date} date1
 * @param {Date} date2
 */
function timeBetween(date1, date2) {
  const d = date2.getTime() - date1.getTime();

  const seconds = Math.floor((d / MS_TO_SECONDS) % 60);
  const minutes = Math.floor((d / MS_TO_MINUTES) % 60);
  const hours = Math.floor((d / MS_TO_HOURS) % 24);
  const days = Math.floor(d / MS_TO_DAYS);

  return {
    days,
    hours,
    minutes,
    seconds,
  };
}

/**
 * @param {Date} date
 */
function countdown(now) {
  const ylonz = document.getElementById("ylonz");
  if (!ylonz) {
    return;
  }

  const ylonzTimeEl = ylonz.querySelector("#ylonz-time");
  const ylonzTime = new Date(ylonzTimeEl.dateTime);

  const timeLeft = timeBetween(now, ylonzTime);

  ylonz.querySelector("#countdown-days").innerHTML = timeLeft.days;
  ylonz.querySelector("#countdown-hours").innerHTML = timeLeft.hours;
  ylonz.querySelector("#countdown-minutes").innerHTML = timeLeft.minutes;
  ylonz.querySelector("#countdown-seconds").innerHTML = timeLeft.seconds;
}

setInterval(() => countdown(new Date()), 1000);
