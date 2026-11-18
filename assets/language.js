// Both editions are complete HTML pages. Carry the current reading position across.
const languageLink = document.querySelector(".language-switch");
const positions = document.querySelectorAll("[data-position][id]");

languageLink.addEventListener("click", () => {
  const mastheadBottom = document.querySelector(".masthead").getBoundingClientRect().bottom;
  let anchor = "";
  for (const section of positions) {
    if (section.getBoundingClientRect().top > mastheadBottom + 30) break;
    anchor = section.id;
  }
  languageLink.hash = anchor;
});
