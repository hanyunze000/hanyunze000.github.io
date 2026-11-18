const languageLink = document.querySelector(".language-switch");
const alternateEdition = languageLink.getAttribute("href");
const header = document.querySelector(".masthead");
const navLinks = [...document.querySelectorAll(".section-nav a")];
const readingAnchors = [...document.querySelectorAll(
  "main section[id], main article[id], #contact"
)].reverse();

new ResizeObserver(() => {
  document.documentElement.style.setProperty("--masthead-height", header.getBoundingClientRect().height + "px");
}).observe(header);

function restorePublicationBookmark() {
  if (!["#chinese-publications", "#international-publications", "#international-publications-heading"].includes(location.hash)) return;
  const url = new URL(location.href);
  url.hash = "publications";
  url.searchParams.delete("open");
  history.replaceState(history.state, "", url);
  document.getElementById("publications").scrollIntoView({behavior: "instant"});
}

function updateNavigation() {
  const boundary = header.getBoundingClientRect().bottom + 38;
  let activeLink = null;
  for (const link of navLinks) {
    if (document.getElementById(link.hash.slice(1)).getBoundingClientRect().top <= boundary) activeLink = link;
  }
  for (const link of navLinks) {
    if (link === activeLink) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  }
}

function readingAnchor() {
  if (window.scrollY <= 12) return null;
  const padding = parseFloat(getComputedStyle(document.documentElement).scrollPaddingTop);
  const boundary = Math.max(header.getBoundingClientRect().bottom, padding) + 2;
  return readingAnchors.find(anchor => anchor.getBoundingClientRect().top <= boundary);
}

function updateLanguageLink() {
  const url = new URL(alternateEdition, location.href);
  const anchor = readingAnchor();
  if (anchor) url.hash = anchor.id;
  languageLink.href = url.href;
}

let pending = false;
function scheduleUpdate() {
  if (pending) return;
  pending = true;
  requestAnimationFrame(() => {
    updateNavigation();
    updateLanguageLink();
    pending = false;
  });
}
window.addEventListener("scroll", scheduleUpdate, {passive: true});
window.addEventListener("resize", scheduleUpdate);
window.addEventListener("hashchange", () => { restorePublicationBookmark(); scheduleUpdate(); });
window.addEventListener("pageshow", scheduleUpdate);
languageLink.addEventListener("click", updateLanguageLink);
restorePublicationBookmark();
scheduleUpdate();
