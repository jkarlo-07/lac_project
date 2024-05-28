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

  document.getElementById("header-weekday").textContent = formattedDay;
  document.getElementById("header-date").textContent = formattedDate;
  document.getElementById("header-time").textContent = formattedTime;
};

updateTime();
setInterval(updateTime, 1000);

const menuButton = document.querySelector(".menu-btn");
const menuNav = document.querySelector(".header-nav");

const toggleMenu = () => {
  menuNav.style.display =
    menuNav.style.display === "none" ||
    getComputedStyle(menuNav).display === "none"
      ? "block"
      : "none";
};

menuButton.addEventListener("click", toggleMenu);

const adjustMenuDisplay = () => {
  menuNav.style.display = window.innerWidth > 900 ? "flex" : "none";
};

adjustMenuDisplay();
window.addEventListener("resize", adjustMenuDisplay);
