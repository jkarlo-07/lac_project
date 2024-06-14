const track = document.querySelector(".event-img-track");
const slides = Array.from(track.children);
const nextButton = document.querySelector(".next");
const prevButton = document.querySelector(".prev");

let slideWidth = slides[0].getBoundingClientRect().width;

const setSlidePosition = (slide, index) => {
  slide.style.left = slideWidth * index + "px";
};

const updateSlidePositions = () => {
  slideWidth = slides[0].getBoundingClientRect().width;
  slides.forEach(setSlidePosition);

  const currentSlide = track.querySelector(".current-slide");
  const currentSlideIndex = slides.findIndex(slide => slide === currentSlide);
  track.style.transform = "translateX(-" + slideWidth * currentSlideIndex + "px)";
};

slides.forEach(setSlidePosition);

const moveToSlide = (track, currentSlide, targetSlide) => {
  track.style.transform = "translateX(-" + targetSlide.style.left + ")";
  currentSlide.classList.remove("current-slide");
  targetSlide.classList.add("current-slide");
};

nextButton.addEventListener("click", (e) => {
  const currentSlide = track.querySelector(".current-slide");
  const nextSlide = currentSlide.nextElementSibling;

  // If there is no next slide, do nothing
  if (!nextSlide) {
    return;
  }

  moveToSlide(track, currentSlide, nextSlide);
});

prevButton.addEventListener("click", (e) => {
  const currentSlide = track.querySelector(".current-slide");
  const prevSlide = currentSlide.previousElementSibling;

  // If there is no previous slide, do nothing
  if (!prevSlide) {
    return;
  }

  moveToSlide(track, currentSlide, prevSlide);
});

window.addEventListener("resize", () => {
  updateSlidePositions();
});
