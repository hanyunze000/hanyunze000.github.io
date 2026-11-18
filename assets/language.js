const languageLink = document.querySelector(".language-switch");
const alternateEdition = languageLink.getAttribute("href");
const header = document.querySelector(".masthead");
const navLinks = [...document.querySelectorAll(".section-nav a")];
const readingAnchors = [...document.querySelectorAll(
  "main section[id], main article[id], #contact, #publications, #chinese-publications"
)].reverse();
const collections = [...document.querySelectorAll("details.collection")];
const defaultPanels = collections.filter(item => item.open).map(item => item.id).join(",");

new ResizeObserver(() => {
  document.documentElement.style.setProperty("--masthead-height", header.getBoundingClientRect().height + "px");
}).observe(header);

function revealBookmark(preservePanel = false) {
  const target = document.getElementById(location.hash.slice(1));
  if (!target) return;
  if (preservePanel && target.matches("details.collection")) return;
  let disclosure = target.closest("details");
  let opened = false;
  while (disclosure) {
    if (!disclosure.open) {
      disclosure.open = true;
      opened = true;
    }
    disclosure = disclosure.parentElement.closest("details");
  }
  if (opened) target.scrollIntoView({behavior: "instant"});
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
  const expanded = collections.filter(item => item.open).map(item => item.id).join(",");
  if (expanded !== defaultPanels || collections.includes(anchor)) {
    url.searchParams.set("open", expanded);
  }
  languageLink.href = url.href;
}

const requested = new URLSearchParams(location.search).get("open");
for (const disclosure of collections) {
  if (requested !== null) disclosure.open = requested.split(",").includes(disclosure.id);
  disclosure.addEventListener("toggle", updateLanguageLink);
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
window.addEventListener("hashchange", () => { revealBookmark(); scheduleUpdate(); });
window.addEventListener("pageshow", scheduleUpdate);
languageLink.addEventListener("click", updateLanguageLink);
revealBookmark(requested !== null);
scheduleUpdate();
