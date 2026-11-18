# Yunze Han

An English and Japanese academic homepage for GitHub Pages. Open `index.html` for English or `ja.html` for Japanese. All public pages, fonts, and the English CV are included in this repository.

## Update the homepage

- Replace `assets/portrait.jpg` with a portrait cropped to 5:6. Update its English and Japanese alt text in `source/build_site.py` when the photograph changes.
- Edit `source/profile_data.py` for papers, author order, corresponding authors, conference appearances, appointments, and contact details. Each conference entry belongs to its paper. Paired text is English first and Japanese second.
- Run `python source/build_site.py` to regenerate both language editions. Run `python source/build_cv.py` to refresh the English CV with ReportLab installed. Commit the edited source and generated files together.

## Publish with GitHub Pages

The public repository is `hanyunze000/hanyunze000.github.io`. Pages serves the root of the `main` branch at [hanyunze000.github.io](https://hanyunze000.github.io/).
