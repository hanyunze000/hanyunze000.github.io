"""Rebuild both static language editions with Python's standard library."""

import json
from hashlib import sha256
from html import escape
from pathlib import Path
from urllib.parse import quote

import profile_data as p


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
            label = local(("(corresponding author)", "（責任著者）"), lang)
            name += f' <span class="author-note" lang="{lang}">{label}</span>'
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
                    f'<div><a href="{escape(meeting["url"])}">{name}</a>{note}{earlier}</div></li>')
    return f'<div class="meetings"><ul>{"".join(rows)}</ul></div>'


def paper_entry(paper, lang, compact=False):
    def tr(en, ja):
        return local((en, ja), lang)

    published = "doi" in paper
    title = escape(paper["title"])
    journal = details = ""
    if published:
        url = "https://doi.org/" + paper["doi"]
        title = f'<a href="{url}">{title}</a>'
        cite = f' · {escape(paper["citation"])}' if "citation" in paper else ""
        journal = (f'<p class="journal"><span class="pub-year">{paper["year"]}</span>'
                   f'<i lang="en">{escape(paper["journal"])}</i>{cite}</p>')
        action = f'<a class="article-link" href="{url}">{tr("Read article", "論文を読む")} <span aria-hidden="true">↗</span></a>'
    else:
        subject = quote("Paper request: " + paper["title"], safe="")
        action = (f'<a class="request-link" href="mailto:{p.EMAIL}?subject={subject}">'
                  f'{tr("Request a draft", "草稿を依頼")} <span aria-hidden="true">↗</span></a>')

    count = len(paper.get("meetings", []))
    if published and not compact:
        detail_text = f'<p class="paper-summary">{escape(local(paper["summary"], lang))}</p>'
        if "earlier_version" in paper:
            detail_text += (f'<a class="version-link" href="{paper["earlier_version"]}">'
                            f'{tr("Discussion paper at Kyoto University", "京都大学のディスカッションペーパー版")} ↗</a>')
        details += f'<details class="disclosure"><summary>{tr("Research summary", "研究概要")}</summary>{detail_text}</details>'
    if count:
        if paper["id"] == "motorway-expansion":
            label = tr("Conference program", "学会プログラム")
        else:
            label = tr(f"Presentations ({count})", f"研究発表（{count}件）")
        details += f'<details class="disclosure"><summary>{label}</summary>{meetings(paper, lang)}</details>'
    return (f'<article class="paper" id="{paper["id"]}" data-position><div class="paper-line">'
            f'<div class="paper-info">{journal}<h3 lang="en">{title}</h3>'
            f'<p class="authors" lang="en">{authors(paper, lang)}</p></div>'
            f'<div class="paper-action">{action}</div></div>'
            f'<div class="paper-details">{details}</div></article>')


def cv_rows(rows, lang):
    entries = []
    for date, title, institution in rows:
        entries.append(f'<li><div><strong>{escape(local(title, lang))}</strong>'
                       f'<span>{escape(local(institution, lang))}</span></div>'
                       f'<span class="cv-date">{escape(local(date, lang))}</span></li>')
    return f'<ul class="cv-rows">{"".join(entries)}</ul>'


PAGES = {
    "home": ("index.html", "ja.html"),
    "research": ("research.html", "research-ja.html"),
    "projects": ("projects.html", "projects-ja.html"),
    "cv": ("cv.html", "cv-ja.html"),
}


def render(lang, page):
    def tr(en, ja):
        return local((en, ja), lang)

    def path(key):
        return local(PAGES[key], lang)

    def section(sid, heading, body, jump=""):
        return (f'<section class="page-section" id="{sid}" aria-labelledby="{sid}-heading" data-position>'
                f'<div class="section-top"><h2 id="{sid}-heading">{heading}</h2>{jump}</div>{body}</section>')

    def page_intro(heading, extra=""):
        return f'<div class="wrap page-intro"><h1>{heading}</h1>{extra}</div>'

    alt_lang = tr("ja", "en")
    name, native = (p.NAME, p.NAME_JA) if lang == "en" else (p.NAME_JA, p.NAME)
    titles = {
        "home": tr("Agricultural and Development Economics", "農業経済学・開発経済学"),
        "research": tr("Research", "研究"), "projects": tr("Research projects", "調査プロジェクト"),
        "cv": tr("Curriculum vitae", "略歴"),
    }
    description = tr(
        "Yunze Han studies agricultural and development economics at Kyoto University. Publications, working papers, field projects, and academic CV.",
        "京都大学大学院で農業経済学・開発経済学を研究する韓運澤のホームページ。学術論文、ワーキングペーパー、調査プロジェクト、略歴を掲載しています。",
    )
    external = '<span class="arrow" aria-hidden="true">↗</span>'
    publications_label = tr("Publications", "学術論文")
    working_label = tr("Working papers", "ワーキングペーパー")
    cv_download = tr("Download CV (PDF)", "英文CV（PDF）")
    download = f'<a class="primary-link" href="assets/yunze-han-cv.pdf">{cv_download} <span aria-hidden="true">↓</span></a>'
    if page == "home":
        hero = f"""
        <section class="profile" aria-labelledby="profile-name"><div class="wrap profile-inner">
          <div class="profile-copy">
            <p class="affiliation">{tr("Kyoto University", "京都大学")}</p>
            <h1 id="profile-name">{name}<span class="other-name" lang="{alt_lang}">{native}</span></h1>
            <p class="role">{local(p.ROLE, lang)}</p>
            <p class="bio">{local(p.BIO, lang)}</p>
            <ul class="profile-links" aria-label="{tr("Contact and research profiles", "連絡先・研究者プロフィール")}">
              <li><a href="mailto:{p.EMAIL}">{tr("Email", "メール")}</a></li>
              <li><a href="{p.RESEARCHMAP}" lang="en">researchmap {external}</a></li>
              <li><a href="{p.ORCID}" lang="en">ORCID {external}</a></li>
            </ul>
          </div>
          <div class="portrait-frame"><img src="assets/portrait.jpg" alt="{tr("Yunze Han in the mountains", "山を背景にした韓運澤の写真")}" width="720" height="864"></div>
        </div></section>"""
        working_link = f'<a class="text-link" href="{path("research")}#working-papers">{working_label} <span aria-hidden="true">→</span></a>'
        entries = "".join(paper_entry(item, lang, compact=True) for item in p.PUBLICATIONS)
        body = hero + '<div class="wrap">' + section("publications", publications_label, entries, working_link) + '</div>'
    elif page == "research":
        contents = (f'<nav class="jump-links" aria-label="{tr("Research sections", "研究の目次")}">'
                    f'<a href="#publications">{publications_label}</a><a href="#working-papers">{working_label}</a></nav>')
        pubs = section("publications", publications_label, "".join(paper_entry(item, lang) for item in p.PUBLICATIONS))
        working = section("working-papers", working_label, "".join(paper_entry(item, lang) for item in p.WORKING_PAPERS))
        body = page_intro(titles[page], contents) + f'<div class="wrap">{pubs}{working}</div>'
    elif page == "projects":
        intro = tr("I work on project evaluations at the JICA Ogata Sadako Research Institute for Peace and Development.",
                   "JICA緒方貞子平和開発研究所で、開発プロジェクトの効果検証に携わっています。")
        projects = []
        for project, sid in zip(p.FIELDWORK, ("sri-lanka", "uganda")):
            heading = escape(local(project["title"], lang))
            detail = escape(local(project["detail"], lang))
            projects.append(f'<article class="project" id="{sid}" data-position><p class="small-label">{local(project["country"], lang)}</p>'
                            f'<div><h2>{heading}</h2><p>{detail}</p></div></article>')
        body = page_intro(titles[page], f'<p class="intro-text">{intro}</p>') + f'<div class="wrap project-list">{"".join(projects)}</div>'
    else:
        groups = [
            ("education", tr("Education", "学歴"), cv_rows(p.EDUCATION, lang)),
            ("interests", tr("Research interests", "研究分野"), f'<p>{local(p.INTERESTS, lang)}</p>'),
            ("appointments", tr("Research, teaching & service", "研究・教育・学内業務"), cv_rows(p.APPOINTMENTS, lang)),
            ("awards", tr("Fellowships & awards", "奨学金・受賞"), cv_rows(p.AWARDS, lang)),
        ]
        memberships = "".join(
            f'<li><span>{escape(local(society, lang))}</span><span class="cv-date">{tr("Since " + year, year + "年より")}</span></li>'
            for year, society in p.MEMBERSHIPS
        )
        groups.extend([
            ("memberships", tr("Academic memberships", "所属学会"), f'<ul class="memberships">{memberships}</ul>'),
            ("other-experience", tr("Other professional experience", "その他の職歴"), cv_rows(p.OTHER_EXPERIENCE, lang)),
        ])
        entries = "".join(f'<section class="cv-group" id="{sid}" data-position><h2>{heading}</h2><div>{html}</div></section>'
                          for sid, heading, html in groups)
        body = page_intro(titles[page], download) + f'<div class="wrap cv-list">{entries}</div>'

    info = {"@context": "https://schema.org", "@type": "Person", "name": p.NAME,
            "alternateName": ["韩运泽", p.NAME_JA], "email": f"mailto:{p.EMAIL}",
            "affiliation": {"@type": "CollegeOrUniversity", "name": "Kyoto University"},
            "sameAs": [p.ORCID, p.RESEARCHMAP]}
    nav = []
    for key, label in (("research", tr("Research", "研究")), ("projects", tr("Projects", "プロジェクト")), ("cv", tr("CV", "略歴"))):
        current = ' aria-current="page"' if page == key else ""
        nav.append(f'<a href="{path(key)}"{current}>{label}</a>')
    extra_contact = f' · <a href="mailto:{p.OTHER_EMAIL}">{p.OTHER_EMAIL}</a>' if page == "cv" else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#fafaf7">
  <meta name="description" content="{escape(description, quote=True)}">
  <title>{tr(p.NAME, p.NAME_JA)} | {titles[page]}</title>
  <link rel="alternate" hreflang="en" href="{PAGES[page][0]}">
  <link rel="alternate" hreflang="ja" href="{PAGES[page][1]}">
  <link rel="alternate" hreflang="x-default" href="{PAGES[page][0]}">
  <link rel="icon" href="assets/favicon.png" type="image/png">
  <link rel="stylesheet" href="{asset("style.css")}">
  <script src="{asset("language.js")}" defer></script>
  <script type="application/ld+json">{json.dumps(info, ensure_ascii=False)}</script>
</head>
<body id="top" class="page-{page}">
  <a class="skip-link" href="#main">{tr("Skip to content", "本文へ移動")}</a>
  <header class="masthead"><div class="wrap masthead-inner">
    <a class="brand" href="{path("home")}" aria-label="{tr("Yunze Han, homepage", "韓運澤のホームページ")}"><span class="seal" aria-hidden="true" lang="ja">韓</span><span lang="en">Yunze Han</span></a>
    <nav aria-label="{tr("Main navigation", "メインナビゲーション")}">{"".join(nav)}
      <a class="language-switch" href="{local(PAGES[page], alt_lang)}" hreflang="{alt_lang}" lang="{alt_lang}"
         aria-label="{tr("日本語で読む", "Read in English")}">{tr("日本語", "English")}</a>
    </nav></div></header>
  <main id="main">{body}</main>
  <footer class="footer"><div class="wrap footer-inner">
    <div><span lang="en">Yunze Han</span><span class="footer-dot" aria-hidden="true"> · </span>{tr("Kyoto University", "京都大学")}
      <p><a href="mailto:{p.EMAIL}">{p.EMAIL}</a>{extra_contact}</p></div>
    <a class="back-link" href="#top">{tr("Back to top", "ページの先頭へ")} ↑</a>
  </div></footer>
</body></html>
"""


if __name__ == "__main__":
    for key, filenames in PAGES.items():
        for language, filename in zip(("en", "ja"), filenames):
            (ROOT / filename).write_text(render(language, key), encoding="utf-8")
