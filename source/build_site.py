"""Rebuild both static language editions with Python's standard library."""

import json
from hashlib import sha256
from html import escape
from pathlib import Path

import profile_data as p
from photographs import ROWS as PHOTO_ROWS


ROOT = Path(__file__).resolve().parent.parent


def asset(name, *, directory="assets"):
    path = Path(directory) / name
    version = sha256((ROOT / path).read_bytes()).hexdigest()[:8]
    return f"{path.as_posix()}?v={version}"


def local(value, lang):
    if isinstance(value, str):
        return value
    return value[0 if lang == "en" else 1]


def prose(value, lang):
    """Keep each supplied phrase together when it fits on a line."""
    text = local(value, lang)
    if isinstance(text, str):
        return escape(text)
    separator = " " if lang == "en" else "<wbr>"
    return separator.join(f'<span class="phrase">{escape(phrase)}</span>' for phrase in text)


def new_tab_attrs(url, lang):
    hint = local(("Open in a new tab", "新しいタブで開く"), lang)
    return f'href="{escape(url, quote=True)}" target="_blank" rel="noopener" title="{hint}"'


def authors(paper, lang):
    names = []
    for author in paper["authors"]:
        name = escape(author)
        if author == p.NAME:
            name = f"<strong>{name}</strong>"
        if author == paper.get("corresponding"):
            label = local(("Corresponding author", "責任著者"), lang)
            name += (f'<sup title="{label}"><span aria-hidden="true">*</span>'
                     f'<span class="sr-only" lang="{lang}"> {label}</span></sup>')
        names.append(f'<span class="paper-author">{name}</span>')
    return ", ".join(names)


def meetings(paper, lang):
    if not paper.get("meetings"):
        return ""
    rows = []
    for meeting in paper["meetings"]:
        name = escape(local(meeting["name"], lang))
        if isinstance(meeting["name"], str):
            name = f'<span lang="en">{name}</span>'
        date = escape(local(meeting["date"], lang))
        note = ""
        if "note" in meeting:
            role = escape(local(meeting["note"], lang))
            note = '<span class="meeting-note">' + local((f" ({role})", f"（{role}）"), lang) + '</span>'
        earlier = ""
        if "earlier_title" in meeting:
            label = local(("Title on the program", "プログラム掲載時の題目"), lang)
            earlier = (f'<details class="early-title"><summary>{label}</summary>'
                       f'<p lang="en">{escape(meeting["earlier_title"])}</p></details>')
        rows.append(f'<li><span class="meeting-date">{date}</span>'
                    f'<div>{name}{note}{earlier}</div></li>')
    return f'<div class="meetings"><ul>{"".join(rows)}</ul></div>'


def paper_entry(paper, lang):
    def tr(en, ja):
        return local((en, ja), lang)

    published = "doi" in paper
    title = escape(paper["title"])
    journal = details = action = ""
    if published:
        link_attrs = new_tab_attrs("https://doi.org/" + paper["doi"], lang)
        title = f'<a {link_attrs}>{title}</a>'
        journal = (f'<p class="journal"><span class="pub-year">{paper["year"]}</span>'
                   f'<i lang="en">{escape(paper["journal"])}</i></p>')
        action = (f'<div class="paper-action"><a class="article-link" {link_attrs}>{tr("Read article", "論文を読む")}'
                  f' <span aria-hidden="true">↗</span></a></div>')

    if published:
        detail_text = f'<p class="paper-summary">{prose(paper["summary"], lang)}</p>'
        details += f'<details class="disclosure"><summary>{tr("Research summary", "論文概要")}</summary>{detail_text}</details>'
    if paper.get("meetings"):
        label = local(p.presentation_heading(paper["meetings"]), lang)
        details += f'<details class="disclosure"><summary>{label}</summary>{meetings(paper, lang)}</details>'
    return (f'<article class="paper" id="{paper["id"]}"><div class="paper-line">'
            f'<div class="paper-info">{journal}<h4 class="paper-title" lang="en">{title}</h4>'
            f'<p class="authors" lang="en">{authors(paper, lang)}</p></div>'
            f'{action}</div>'
            f'<div class="paper-details">{details}</div></article>')


def cv_date(value, lang):
    date = local(value, lang)
    if isinstance(date, str):
        return escape(date)
    start, end, note = map(escape, date)
    return (f'<span class="date-range"><span>{start} –</span> <span>{end}</span>'
            f' <small>{note}</small></span>')


def cv_rows(rows, lang):
    entries = []
    for date, title, institution, *details in rows:
        description = "".join(f'<p class="cv-detail">{prose(item, lang)}</p>' for item in details)
        entries.append(f'<li><div><strong>{escape(local(title, lang))}</strong>'
                       f'<span>{escape(local(institution, lang))}</span>{description}</div>'
                       f'<span class="cv-date">{cv_date(date, lang)}</span></li>')
    return f'<ul class="cv-rows">{"".join(entries)}</ul>'


EDITIONS = {"en": "index.html", "ja": "ja.html"}


def photography(lang):
    def tr(en, ja):
        return local((en, ja), lang)

    rows = []
    for row in PHOTO_ROWS:
        links = []
        for photo in row:
            base = f"assets/photography/{photo.slug}"
            ratio = photo.width / photo.height
            links.append(
                f'<a class="gallery-photo" href="{base}.jpg" style="--ratio:{ratio:.5f}">'
                f'<img src="assets/photography/previews/{photo.slug}.webp" width="{photo.width}" height="{photo.height}" '
                f'loading="lazy" decoding="async" alt="{escape(local(photo.description, lang), quote=True)}"></a>'
            )
        rows.append(f'<div class="photo-row">{"".join(links)}</div>')
    return f"""<div class="photo-gallery">{"".join(rows)}</div>
        <dialog class="photo-viewer" aria-label="{tr("Photograph viewer", "写真の拡大表示")}">
          <div class="viewer-bar"><div class="viewer-navigation">
            <button type="button" data-step="-1" aria-label="{tr("Previous photograph", "前の写真")}">←</button>
            <span class="viewer-count" aria-live="polite" aria-atomic="true"></span>
            <button type="button" data-step="1" aria-label="{tr("Next photograph", "次の写真")}">→</button>
          </div><form method="dialog"><button autofocus>{tr("Close", "閉じる")} <span aria-hidden="true">×</span></button></form></div>
          <img class="viewer-image" alt="">
        </dialog>"""


def render(lang, edition_query=""):
    def tr(en, ja):
        return local((en, ja), lang)

    def cv_section(sid, heading, content):
        return (f'<section class="cv-group" id="{sid}" aria-labelledby="{sid}-heading">'
                f'<h2 id="{sid}-heading">{heading}</h2><div>{content}</div></section>')

    alt_lang = tr("ja", "en")
    name, native = (p.NAME, p.NAME_JA) if lang == "en" else (p.NAME_JA, p.NAME)
    interests = prose((
        ("My research interests are", "development economics", "and agricultural economics."),
        ("専門は開発経済学と", "農業経済学です。"),
    ), lang)
    description = tr("Yunze Han at Kyoto University. Publications, working papers, education, and research projects.",
                     "京都大学大学院農学研究科の韓運澤の個人サイト。開発経済学・農業経済学の論文と研究プロジェクトを紹介しています。")
    info = {"@context": "https://schema.org", "@type": "Person", "name": p.NAME,
            "alternateName": ["韩运泽", p.NAME_JA],
            "affiliation": {"@type": "CollegeOrUniversity", "name": "Kyoto University"},
            "sameAs": [p.RESEARCHMAP]}
    arrow = '<span class="arrow" aria-hidden="true">↗</span>'
    labels = {
        "education": tr("Education", "学歴"), "research": tr("Research", "研究"),
        "projects": tr("Projects", "研究プロジェクト"), "experience": tr("Experience", "経歴"),
        "photography": tr("Photography", "写真作品"),
    }
    nav = "".join(f'<a href="#{sid}">{label}</a>' for sid, label in labels.items())
    pubs = "".join(paper_entry(item, lang) for item in p.PUBLICATIONS)
    working = "".join(paper_entry(item, lang) for item in p.WORKING_PAPERS)
    education = cv_section("education", labels["education"], cv_rows(p.EDUCATION, lang))

    project_intro = prose((
        f"At the {p.JICA[0]}, I help evaluate agricultural development projects.",
        (f"{p.JICA[1]}で、", "農業開発事業の評価に取り組んでいます。"),
    ), lang)
    projects = []
    for project, sid in zip(p.FIELDWORK, ("sri-lanka", "uganda")):
        projects.append(f'<article class="project" id="{sid}">'
                        f'<p class="small-label">{escape(local(project["country"], lang))}</p>'
                        f'<div><h3>{prose(project["title"], lang)}</h3>'
                        f'<p>{prose(project["detail"], lang)}</p></div></article>')

    memberships = "".join(
        f'<li><span>{escape(local(society, lang))}</span><span class="cv-date">{tr("Since " + year, year + "年より")}</span></li>'
        for year, society in p.MEMBERSHIPS
    )
    experience = [
        ("teaching", tr("Teaching experience", "教育歴"), cv_rows(p.TEACHING, lang)),
        ("appointments", tr("Research &amp; university service", "研究・学内業務"), cv_rows(p.APPOINTMENTS, lang)),
        ("awards", tr("Fellowships &amp; awards", "奨学金・受賞歴"), cv_rows(p.AWARDS, lang)),
        ("memberships", tr("Academic memberships", "所属学会"), f'<ul class="memberships">{memberships}</ul>'),
        ("languages", tr("Languages", "語学資格"), f'<p>{escape(local(p.LANGUAGE_QUALIFICATION, lang))}</p>'),
        ("other-experience", tr("Other professional experience", "その他の職歴"), cv_rows(p.OTHER_EXPERIENCE, lang)),
    ]
    background = "".join(f'<section class="cv-group" id="{sid}" aria-labelledby="{sid}-heading">'
                         f'<h3 id="{sid}-heading">{label}</h3><div>{content}</div></section>'
                         for sid, label, content in experience)
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#fafaf7">
  <meta name="description" content="{escape(description, quote=True)}">
  <title>{name} | {tr("Academic homepage", "研究者ホームページ")}</title>
  <link rel="alternate" hreflang="en" href="index.html">
  <link rel="alternate" hreflang="ja" href="ja.html">
  <link rel="alternate" hreflang="x-default" href="index.html">
  <link rel="icon" href="{asset('favicon.png')}" type="image/png" sizes="128x128">
  <link rel="icon" href="{asset('favicon.ico', directory='.')}" type="image/x-icon" sizes="16x16 32x32 48x48 64x64">
  <link rel="stylesheet" href="{asset("style.css")}">
  <script src="{asset("language.js")}" defer></script>
  <script src="{asset("gallery.js")}" defer></script>
  <script type="application/ld+json">{json.dumps(info, ensure_ascii=False)}</script>
</head>
<body id="top">
  <a class="skip-link" href="#main">{tr("Skip to content", "本文へ移動")}</a>
  <header class="masthead"><div class="wrap masthead-inner">
    <a class="brand" href="#top" aria-label="{tr("Yunze Han, homepage", "韓運澤のホームページ")}"><span class="seal" aria-hidden="true" lang="ja">韓</span><span lang="en">Yunze Han</span></a>
    <nav class="section-nav" aria-label="{tr("Main navigation", "メインナビゲーション")}">{nav}</nav>
    <a class="language-switch" href="{EDITIONS[alt_lang]}{edition_query}" hreflang="{alt_lang}" lang="{alt_lang}" aria-label="{tr("日本語で読む", "Read in English")}">{tr("日本語", "English")}</a>
  </div></header>
  <main id="main">
    <section class="profile" aria-labelledby="profile-name"><div class="wrap profile-inner">
      <div class="profile-copy">
        <h1 id="profile-name">{name}<span class="other-name" lang="{alt_lang}">{native}</span></h1>
        <div id="contact" class="contact">
          <p class="research-interests">{interests}</p>
          <p><span class="contact-label">{tr("Email", "メール")}</span> <span class="email-address" dir="ltr">{p.MASKED_EMAIL}</span></p>
          <p class="contact-hint">{tr("Replace * with @ when emailing.", "送信時は * を @ に置き換えてください。")}</p>
        </div>
        <ul class="profile-links" aria-label="{tr("Research profiles", "研究者プロフィール")}">
          <li><a {new_tab_attrs(p.RESEARCHMAP, lang)} lang="en">researchmap {arrow}</a></li>
        </ul>
      </div>
      <div class="portrait-frame"><img src="assets/portrait.jpg" alt="{tr("Yunze Han in the mountains", "山を背景にした韓運澤の写真")}" width="720" height="864"></div>
    </div></section>
    <div class="wrap page-content">
      {education}
      <section class="page-section" id="research" aria-labelledby="research-heading">
        <h2 id="research-heading">{labels["research"]}</h2>
        <section id="publications" class="publications" aria-labelledby="publications-heading">
          <div class="subsection-head"><h3 id="publications-heading">{tr("Publications", "学術論文")} <span class="count">({len(p.PUBLICATIONS)})</span></h3>
            <p class="paper-key"><span aria-hidden="true">*</span> {tr("Corresponding author", "責任著者")}</p></div>
          {pubs}
        </section>
        <section id="working-papers" class="working-papers" aria-labelledby="working-papers-heading">
          <h3 id="working-papers-heading">{tr("Working papers", "ワーキングペーパー")} <span class="count">({len(p.WORKING_PAPERS)})</span></h3>
          {working}
        </section>
      </section>
      <section class="page-section" id="projects" aria-labelledby="projects-heading">
        <h2 id="projects-heading">{tr("Research projects", "研究プロジェクト")}</h2>
        <p class="section-intro">{project_intro}</p>
        {"".join(projects)}
      </section>
      <section class="page-section experience" id="experience" aria-labelledby="experience-heading">
        <h2 id="experience-heading">{labels["experience"]}</h2>{background}
      </section>
      <section class="page-section" id="photography" aria-labelledby="photography-heading">
        <h2 id="photography-heading">{labels["photography"]}</h2>
        {photography(lang)}
      </section>
    </div>
  </main>
  <footer class="footer"><div class="wrap footer-inner">
    <a {new_tab_attrs(asset("yunze-han-cv.pdf"), lang)}>{tr("Download CV (PDF)", "英文CV（PDF）")} <span aria-hidden="true">↓</span></a>
    <a class="back-link" href="#top">{tr("Back to top", "ページの先頭へ")} ↑</a>
  </div></footer>
</body></html>
"""


def redirect(lang, default_section):
    """Keep published bookmarks to the earlier multi-page site working."""
    home = EDITIONS[lang]
    url = home + "#" + default_section
    label = local(("Go to the homepage", "ホームページへ移動"), lang)
    return f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{local((p.NAME, p.NAME_JA), lang)}</title><link rel="canonical" href="https://hanyunze000.github.io/{home}">
<script>
const oldAnchor = location.hash;
const section = !oldAnchor || ["#interests", "#top", "#main"].includes(oldAnchor) ? "#{default_section}" : oldAnchor;
location.replace("{home}" + section);
</script><noscript><meta http-equiv="refresh" content="0;url={url}"></noscript></head>
<body><p><a href="{url}">{label}</a></p></body></html>
"""


if __name__ == "__main__":
    # Hash both editions before inserting their cross-links to avoid a circular dependency.
    editions = "".join(render(language) for language in EDITIONS)
    edition_query = "?v=" + sha256(editions.encode("utf-8")).hexdigest()[:8]
    for language, filename in EDITIONS.items():
        (ROOT / filename).write_text(render(language, edition_query), encoding="utf-8")
        suffix = "-ja" if language == "ja" else ""
        for legacy, section in (("research", "research"), ("projects", "projects"), ("cv", "education")):
            (ROOT / f"{legacy}{suffix}.html").write_text(redirect(language, section), encoding="utf-8")
