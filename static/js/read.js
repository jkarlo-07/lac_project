const roomDiv = document.querySelector(".room-expand-small");
const readButton = document.querySelector(".expand-button-hidden");
const secondParagraph = roomDiv.querySelectorAll('p')[1];
secondParagraph.style.display = "none";


readButton.addEventListener("click", function () {
    event.preventDefault();
    if (readButton.textContent === "Read Less") {
        secondParagraph.style.display = "none";
        readButton.textContent = "Read More";
    } else {
        secondParagraph.style.display = "block";
        readButton.textContent = "Read Less";
    }
})




