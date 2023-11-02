document.getElementById("form").addEventListener("submit", (e) => {
  e.preventDefault();
  const image = document.getElementById("file").files[0];

  const form_data = new FormData();

  form_data.append("image", image);

  fetch("http://localhost:5000/compress", {
    method: "POST",
    body: form_data,
  })
    .then((res) => res.json())
    .then((data) => console.log(data))
    .catch((err) => console.log(err));
});
