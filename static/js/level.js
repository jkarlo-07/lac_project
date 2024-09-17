document.addEventListener("DOMContentLoaded", function () {

    function handleResize() {
        window.addEventListener("resize", function () {
            const sidebar = document.querySelector('.booking-page-sidebar');
            const bookingContainer = document.querySelector('.booking_container_main');
            const bookingWrapper = document.querySelector('.booking-page-wrapper');
            if (window.innerWidth < 1024 && sidebar.classList.contains("atWrapper")) {
                console.log("less than 1024");
                sidebar.classList.add("atContainer");
                sidebar.classList.remove("atWrapper");
                bookingWrapper.removeChild(sidebar);
                bookingContainer.appendChild(sidebar);
                bookingContainer.insertBefore(sidebar, bookingContainer.children[1]);
            } else if (window.innerWidth > 1024 && sidebar.classList.contains("atContainer")){
                console.log("less than 1024");
                sidebar.classList.add("atWrapper");
                sidebar.classList.remove("atContainer");
                bookingContainer.removeChild(sidebar);
                bookingWrapper.appendChild(sidebar);
            }
        });
    }
    handleResize();
});
