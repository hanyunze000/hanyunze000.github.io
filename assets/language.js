const languageLink = document.querySelector(".language-switch");
const alternateEdition = languageLink.getAttribute("href");
const header = document.querySelector(".masthead");
const navLinks = [...document.querySelectorAll(".section-nav a")];
const collections = [...document.querySelectorAll("details.collection")];
const defaultPanels = collections.filter(item => item.open).map(item => item.id).join(",");

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

function updateLanguageLink() {
  const url = new URL(alternateEdition, location.href);
  const expanded = collections.filter(item => item.open).map(item => item.id).join(",");
  if (expanded !== defaultPanels) url.searchParams.set("open", expanded);
  if (location.hash && document.getElementById(location.hash.slice(1))) {
    url.hash = location.hash;
  } else if (window.scrollY > 12) {
    const current = navLinks.find(link => link.hasAttribute("aria-current"));
    if (current) url.hash = current.hash;
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
