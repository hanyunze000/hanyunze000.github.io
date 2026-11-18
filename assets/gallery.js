const photoGallery = document.querySelector(".photo-gallery");
const viewer = document.querySelector(".photo-viewer");

if (photoGallery && viewer && typeof viewer.showModal === "function") {
  const photos = [...photoGallery.querySelectorAll(".gallery-photo")];
  const fullImage = viewer.querySelector(".viewer-image");
  const count = viewer.querySelector(".viewer-count");
  let current = 0;

  function showPhoto(index) {
    current = (index + photos.length) % photos.length;
    const link = photos[current];
    fullImage.alt = link.querySelector("img").alt;
    fullImage.src = link.href;
    count.textContent = (current + 1) + " / " + photos.length;
  }

  photoGallery.addEventListener("click", event => {
    const link = event.target.closest(".gallery-photo");
    if (!link || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    showPhoto(photos.indexOf(link));
    viewer.showModal();
    document.documentElement.classList.add("photo-open");
  });

  viewer.addEventListener("click", event => {
    const button = event.target.closest("[data-step]");
    if (button) showPhoto(current + Number(button.dataset.step));
    if (event.target === viewer) {
      const box = viewer.getBoundingClientRect();
      if (event.clientX < box.left || event.clientX > box.right || event.clientY < box.top || event.clientY > box.bottom) {
        viewer.close();
      }
    }
  });
  viewer.addEventListener("keydown", event => {
    if (event.key !== "ArrowRight" && event.key !== "ArrowLeft") return;
    event.preventDefault();
    showPhoto(current + (event.key === "ArrowRight" ? 1 : -1));
  });
  viewer.addEventListener("close", () => {
    document.documentElement.classList.remove("photo-open");
    fullImage.removeAttribute("src");
  });
}
