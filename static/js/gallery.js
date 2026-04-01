const items = document.querySelectorAll(".scroll-gallery .media");

const observer = new IntersectionObserver(
  entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("show");

        // play video if it's a video
        if (entry.target.tagName === "VIDEO") {
          entry.target.play();
        }
      } else {
        // pause video when out of view
        if (entry.target.tagName === "VIDEO") {
          entry.target.pause();
        }
      }
    });
  },
  { threshold: 0.5 }
);

items.forEach(item => observer.observe(item));