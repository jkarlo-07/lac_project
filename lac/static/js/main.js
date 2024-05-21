const updateTime = () => {
  const currentDate = new Date();

  const dateFormatOptions = {
    year: "numeric",
    month: "long",
    day: "numeric",
  };

  const timeFormatOptions = {
    hour: "numeric",
    minute: "numeric",
    hour12: true,
  };

  const formattedDate = currentDate.toLocaleDateString(
    "en-US",
    dateFormatOptions
  );
  const formattedDay = currentDate.toLocaleDateString("en-US", {
    weekday: "long",
  });
  const formattedTime = currentDate.toLocaleTimeString(
    "en-US",
    timeFormatOptions
  );

  const weekdayElement = document.getElementById("header-weekday");
  const dateElement = document.getElementById("header-date");
  const timeElement = document.getElementById("header-time");

  weekdayElement.textContent = formattedDay;
  dateElement.textContent = formattedDate;
  timeElement.textContent = formattedTime;
};

updateTime();
setInterval(updateTime, 1000);
