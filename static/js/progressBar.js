function startProgressBar() {
  const _progressBar = document.querySelector(".progress-bar");
  const progress = document.querySelector(".progress");
  const card = document.querySelector(".card");
  const progressText = document.querySelector(".progress-text");
  let width = 1;

  const interval = setInterval(function () {
    if (width >= 100) {
      clearInterval(interval);
      _progressBar.style.display = "none";
      card.classList.remove("off");
    } else {
      width++;
      progress.style.width = width + "%";
      progressText.textContent = width + "%"; // Update the text with the percentage
    }
  }, 50);
}

window.onload = startProgressBar;
