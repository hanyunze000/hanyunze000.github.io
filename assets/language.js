// Both editions use the same section and paper anchors.
const languageLink = document.querySelector(".language-switch");

function syncSection() {
  languageLink.hash = location.hash;
}

window.addEventListener("hashchange", syncSection);
window.addEventListener("pageshow", syncSection);
syncSection();
