// This JavaScript code enhances the functionality of the landing page.

document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const compressedImage = document.getElementById("compressed-image");
  const downloadLink = document.getElementById("download-link");

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const imageInput = document.getElementById("image");
    const outputImage = document.getElementById("output-image");
    outputImage.style.display = "none";

    const formData = new FormData(form);

    fetch("http://localhost:5000/compress", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          compressedImage.src = data.compressed_url;
          outputImage.style.display = "block";
          downloadLink.href = data.compressed_url;
        }
      })
      .catch((error) => console.error(error));
  });
});
