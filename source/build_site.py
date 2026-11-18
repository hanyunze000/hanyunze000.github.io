"""Rebuild both static language editions with Python's standard library."""

import json
from hashlib import sha256
from html import escape
from pathlib import Path

import profile_data as p
from photographs import ROWS as PHOTO_ROWS


ROOT = Path(__file__).resolve().parent.parent


def asset(name):
    version = sha256((ROOT / "assets" / name).read_bytes()).hexdigest()[:8]
    return f"assets/{name}?v={version}"


def local(value, lang):
    if isinstance(value, str):
        return value
    return value[0 if lang == "en" else 1]


def authors(paper, lang):
    names = []
    for author in paper["authors"]:
        name = escape(author)
        if author == p.NAME:
            name = f"<strong>{name}</strong>"
        if author == paper.get("corresponding"):
            label = local(("Corresponding author", "責任著者"), lang)
            name = (f'<span class="marked-author">{name}<sup title="{label}">'
                    f'<span aria-hidden="true">*</span><span class="sr-only" lang="{lang}"> {label}</span></sup></span>')
        names.append(name)
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
            note = f' <span class="meeting-note">({escape(local(meeting["note"], lang))})</span>'
        earlier = ""
        if "earlier_title" in meeting:
            label = local(("Title on the program", "プログラム上の演題"), lang)
            earlier = (f'<details class="early-title"><summary>{label}</summary>'
                       f'<p lang="en">{escape(meeting["earlier_title"])}</p></details>')
        rows.append(f'<li><span class="meeting-date">{date}</span>'
                    f'<div>{name}{note}{earlier}</div></li>')
    return f'<div class="meetings"><ul>{"".join(rows)}</ul></div>'


def paper_entry(paper, lang):
    def tr(en, ja):
        return local((en, ja), lang)

    published = "doi" in paper
    heading = "h5" if published else "h4"
    title = escape(paper["title"])
    journal = details = action = ""
    if published:
        url = "https://doi.org/" + paper["doi"]
        title = f'<a href="{url}">{title}</a>'
        journal = (f'<p class="journal"><span class="pub-year">{paper["year"]}</span>'
                   f'<i lang="en">{escape(paper["journal"])}</i></p>')
        action = (f'<div class="paper-action"><a class="article-link" href="{url}" target="_blank" rel="noopener" '
                  f'title="{tr("Open in a new tab", "新しいタブで開く")}">{tr("Read article", "論文を読む")}'
                  f' <span aria-hidden="true">↗</span></a></div>')

    count = len(paper.get("meetings", []))
    if published:
        detail_text = f'<p class="paper-summary">{escape(local(paper["summary"], lang))}</p>'
        details += f'<details class="disclosure"><summary>{tr("Research summary", "研究概要")}</summary>{detail_text}</details>'
    if count:
        if paper.get("program_only"):
            label = tr("Conference for this paper", "この論文に関連する学会")
        else:
            label = tr(f"Presentations of this paper ({count})", f"この論文の研究発表（{count}件）")
        details += f'<details class="disclosure"><summary>{label}</summary>{meetings(paper, lang)}</details>'
    return (f'<article class="paper" id="{paper["id"]}"><div class="paper-line">'
            f'<div class="paper-info">{journal}<{heading} class="paper-title" lang="en">{title}</{heading}>'
            f'<p class="authors" lang="en">{authors(paper, lang)}</p></div>'
            f'{action}</div>'
            f'<div class="paper-details">{details}</div></article>')


def cv_rows(rows, lang):
    entries = []
    for date, title, institution in rows:
        entries.append(f'<li><div><strong>{escape(local(title, lang))}</strong>'
                       f'<span>{escape(local(institution, lang))}</span></div>'
                       f'<span class="cv-date">{escape(local(date, lang))}</span></li>')
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


def chinese_publications(lang):
    label = local(("Chinese-language publications", "中国語の掲載論文"), lang)
    records = []
    for item in p.CHINESE_PUBLICATIONS:
        title = escape(item["title"])
        if item.get("translated_title"):
            translation = escape(local(item["translated_title"], lang))
            parenthetical = f" ({translation})" if lang == "en" else f"（{translation}）"
            title += f'<span class="title-translation" lang="{lang}">{parenthetical}</span>'
        if item.get("url"):
            title = f'<a href="{escape(item["url"], quote=True)}">{title}</a>'
        names = "、".join(f'<strong>{escape(name)}</strong>' if name == "韩运泽" else escape(name)
                         for name in item["authors"])
        records.append(f'<li><h5 class="chinese-title">{title}</h5><p class="chinese-citation">'
                       f'{names} · 《{escape(item["journal"])}》 · '
                       f'<span lang="{lang}">{escape(local(p.issue_citation(item), lang))}</span></p></li>')
    return (f'<details id="chinese-publications" class="chinese-pubs collection">'
            f'<summary class="publication-group-heading"><h4>{label} <span class="count">({len(records)})</span></h4></summary>'
            f'<ul class="chinese-list" lang="zh-Hans">{"".join(records)}</ul></details>')


def render(lang):
    def tr(en, ja):
        return local((en, ja), lang)

    def cv_section(sid, heading, content):
        return (f'<section class="cv-group" id="{sid}" aria-labelledby="{sid}-heading">'
                f'<h2 id="{sid}-heading">{heading}</h2><div>{content}</div></section>')

    alt_lang = tr("ja", "en")
    name, native = (p.NAME, p.NAME_JA) if lang == "en" else (p.NAME_JA, p.NAME)
    description = tr("Yunze Han at Kyoto University. Publications, working papers, education, and field projects.",
                     "京都大学の韓運澤の個人ページ。学歴、論文、ワーキングペーパー、調査プロジェクトを掲載しています。")
    info = {"@context": "https://schema.org", "@type": "Person", "name": p.NAME,
            "alternateName": ["韩运泽", p.NAME_JA],
            "affiliation": {"@type": "CollegeOrUniversity", "name": "Kyoto University"},
            "sameAs": [p.RESEARCHMAP]}
    arrow = '<span class="arrow" aria-hidden="true">↗</span>'
    labels = {
        "education": tr("Education", "学歴"), "research": tr("Research", "研究"),
        "projects": tr("Projects", "プロジェクト"), "experience": tr("Experience", "経歴"),
        "photography": tr("Photography", "写真作品"),
    }
    nav = "".join(f'<a href="#{sid}">{label}</a>' for sid, label in labels.items())
    pubs = "".join(paper_entry(item, lang) for item in p.PUBLICATIONS)
    working = "".join(paper_entry(item, lang) for item in p.WORKING_PAPERS)
    education = cv_section("education", labels["education"], cv_rows(p.EDUCATION, lang))

    projects = []
    for project, sid in zip(p.FIELDWORK, ("sri-lanka", "uganda")):
        projects.append(f'<article class="project" id="{sid}">'
                        f'<p class="small-label">{escape(local(project["country"], lang))}</p>'
                        f'<div><h3>{escape(local(project["title"], lang))}</h3>'
                        f'<p>{escape(local(project["detail"], lang))}</p></div></article>')

    memberships = "".join(
        f'<li><span>{escape(local(society, lang))}</span><span class="cv-date">{tr("Since " + year, year + "年より")}</span></li>'
        for year, society in p.MEMBERSHIPS
    )
    experience = [
        ("appointments", tr("Research, teaching &amp; service", "研究・教育・学内業務"), cv_rows(p.APPOINTMENTS, lang)),
        ("awards", tr("Fellowships &amp; awards", "奨学金・受賞"), cv_rows(p.AWARDS, lang)),
        ("memberships", tr("Academic memberships", "所属学会"), f'<ul class="memberships">{memberships}</ul>'),
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
  <link rel="icon" href="assets/favicon.png" type="image/png">
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
    <a class="language-switch" href="{EDITIONS[alt_lang]}" hreflang="{alt_lang}" lang="{alt_lang}" aria-label="{tr("日本語で読む", "Read in English")}">{tr("日本語", "English")}</a>
  </div></header>
  <main id="main">
    <section class="profile" aria-labelledby="profile-name"><div class="wrap profile-inner">
      <div class="profile-copy">
        <h1 id="profile-name">{name}<span class="other-name" lang="{alt_lang}">{native}</span></h1>
        <div id="contact" class="contact">
          <p><span class="contact-label">{tr("Email", "メール")}</span> <span class="email-address" dir="ltr">{p.MASKED_EMAIL}</span></p>
          <p class="contact-hint">{tr("Replace * with @ when emailing.", "送信時は * を @ に置き換えてください。")}</p>
        </div>
        <ul class="profile-links" aria-label="{tr("Research profiles", "研究者プロフィール")}">
          <li><a href="{p.RESEARCHMAP}" lang="en">researchmap {arrow}</a></li>
        </ul>
      </div>
      <div class="portrait-frame"><img src="assets/portrait.jpg" alt="{tr("Yunze Han in the mountains", "山を背景にした韓運澤の写真")}" width="720" height="864"></div>
    </div></section>
    <div class="wrap page-content">
      {education}
      <section class="page-section" id="research" aria-labelledby="research-heading">
        <h2 id="research-heading">{labels["research"]}</h2>
        <div id="publications" class="publications">
          <div class="subsection-head"><h3>{tr("Publications", "学術論文")}</h3>
            <p class="paper-key"><span aria-hidden="true">*</span> {tr("Corresponding author", "責任著者")}</p></div>
          <section id="international-publications" aria-labelledby="international-publications-heading">
            <h4 class="publication-group-heading" id="international-publications-heading">{tr("International peer-reviewed publications", "査読付き国際誌の掲載論文")}</h4>
            {pubs}
          </section>
          {chinese_publications(lang)}
        </div>
        <section id="working-papers" class="working-papers" aria-labelledby="working-papers-heading">
          <h3 id="working-papers-heading">{tr("Working papers", "ワーキングペーパー")} <span class="count">({len(p.WORKING_PAPERS)})</span></h3>
          {working}
        </section>
      </section>
      <section class="page-section" id="projects" aria-labelledby="projects-heading">
        <h2 id="projects-heading">{tr("Research projects", "調査プロジェクト")}</h2>
        <p class="section-intro">{tr("I work on project evaluations at the JICA Ogata Sadako Research Institute for Peace and Development.", "JICA緒方貞子平和開発研究所で、開発プロジェクトの効果検証に携わっています。")}</p>
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
    <a href="{asset("yunze-han-cv.pdf")}">{tr("Download CV (PDF)", "英文CV（PDF）")} <span aria-hidden="true">↓</span></a>
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
    for language, filename in EDITIONS.items():
        (ROOT / filename).write_text(render(language), encoding="utf-8")
        suffix = "-ja" if language == "ja" else ""
        for legacy, section in (("research", "research"), ("projects", "projects"), ("cv", "education")):
            (ROOT / f"{legacy}{suffix}.html").write_text(redirect(language, section), encoding="utf-8")
