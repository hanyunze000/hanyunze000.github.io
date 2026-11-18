# Yunze Han

An English and Japanese academic homepage for GitHub Pages. Each edition presents education, research, projects, experience, and photography on one page. Open `index.html` for English or `ja.html` for Japanese. Links to the former research, projects, and CV pages forward to the corresponding sections.

## Update the homepage

- Replace `assets/portrait.jpg` with a portrait cropped to 5:6. Update its English and Japanese alt text in `source/build_site.py` when the photograph changes.
- Edit `source/profile_data.py` for papers, author order, corresponding authors, conference appearances, appointments, and the masked contact address. Each conference entry belongs to its paper. Paired text is English first and Japanese second.
- The photography gallery uses the rows in `source/photographs.py`. Its descriptions are accessible image alternatives. After changing the collection, run `python source/prepare_photos.py "../摄影作品"` with Pillow installed. This keeps JPEGs up to 5,000,000 bytes intact, compresses larger ones, and creates lightweight previews.
- With ReportLab installed, run `python source/build_cv.py` to update the downloadable CV, then `python source/build_site.py` to regenerate the pages and their versioned asset links. Commit the edited source and generated files together.

## Publish with GitHub Pages

The public repository is `hanyunze000/hanyunze000.github.io`. Pages serves the root of the `main` branch at [hanyunze000.github.io](https://hanyunze000.github.io/).
