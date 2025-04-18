document.addEventListener('DOMContentLoaded', function () {
  const videos = document.querySelectorAll('video');
  const radioButtons = document.querySelectorAll('input[type="radio"]');
  const cards = document.querySelectorAll('.card');

  // Pause and reset video when not in foreground
  function pauseAllVideos() {
    videos.forEach((video) => {
      video.pause();
      video.currentTime = 0;
    });
  }

  // Play the first video on page load with a slight delay
  function playFrontVideo() {
    const firstCard = cards[0];
    const firstVideo = firstCard.querySelector('video');
    if (firstVideo) {
      setTimeout(() => {firstVideo.play();}, 1500); 
    }
  }

  // Play video in foreground when rotating carousel
  function rotateCarousel() {
    radioButtons.forEach((radio, index) => {
      radio.addEventListener('change', () => {
        pauseAllVideos();
        const activeVideo = cards[index].querySelector('video');
        if (activeVideo) {
          activeVideo.play();
        }
      });
    });
  }

  pauseAllVideos();
  playFrontVideo();

  rotateCarousel();
});

// Give scroll down arrow a bounce animation after it initially fades in
document.addEventListener('DOMContentLoaded', () => {
  const arrow = document.querySelector('.scroll-arrow');

  arrow.addEventListener('animationend', () => {
    arrow.style.animation = 'bounce 1.8s infinite';
  });
});


new fullScroll({
  mainElement: "main",
  displayDots: true,
  dotsPosition: "left",
  animateTime: 0.8,
  animateFunction: "ease-in-out",
});