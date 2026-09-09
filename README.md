# Fall 2026 Lab

Course repository for lab exercises, project files, and notes from the Fall 2026 lab course.

**Website:** [ixthecreator.github.io/fall-2026-lab](https://ixthecreator.github.io/fall-2026-lab/)

## Contents

- [`labs/`](labs/) — Lab exercises, experiments, and submissions.
- [`notes/`](notes/) — Course notes and references.
- [`index.html`](index.html) — The course homepage.
- [`styles.css`](styles.css) — The homepage styles, including mobile layouts.
- [`favicon.svg`](favicon.svg) — The browser tab icon.

## Adding coursework

Add a folder for each assignment inside `labs/`, such as `labs/lab-01/`, and include the assignment files and a short README. Save course notes in `notes/`. Update the links and status text in `index.html` as work is added.

## Editing the page

Edit `index.html` to change the text and links, or `styles.css` to change the appearance. The site uses plain HTML and CSS, so there are no dependencies or build steps.

Open `index.html` in a browser to preview it locally, or run:

```sh
python3 -m http.server 8000
```

Then visit [localhost:8000](http://localhost:8000).

## GitHub Pages

The site is published from **main → /(root)** using **Deploy from a branch** in the repository's **Settings → Pages**. Changes pushed to `main` automatically update the site. Check the repository's **Actions** tab for deployment progress.

The published URL is also listed in the repository's **About** section.
