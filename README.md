# shuklock.github.io

The site for Shuklock's WoW Forever kits: https://shuklock.github.io

## Editing

Edit in [Pages CMS](https://app.pagescms.org): sign in with GitHub and open this repo. Every save is a commit to `main`, and GitHub Pages republishes the site a minute or two later.

- **Kits** has one entry per kit. Each kit has its header details (status, version, tagline, icon, CurseForge link) and a list of **Sections** you can add, drag to reorder, or delete:
  - **Text**: a heading and formatted text.
  - **GIF / image / video**: one GIF, image or `.mp4`, full width or beside some text. An `.mp4` plays on loop like a GIF and is usually a tenth the size.
  - **Gallery**: several GIFs or images side by side.
  - **Feature list**: cards with a title, short text and an optional icon.
  - **Callout box**: a highlighted note, tip or warning.
- **Home page** has the big heading and intro text. The kit cards on it come from the Kits entries, sorted by their position number.
- Uploads go in `media/`.

To add a kit, create a new entry under **Kits**. Its page address comes from its name (Druid Kit → `/druid-kit/`).

## Layout

- `_kits/` — one Markdown file per kit; the sections live in its front matter.
- `_layouts/`, `_includes/blocks/` — page templates, one template per section type.
- `assets/css/site.css` — styles.
- `.pages.yml` — the Pages CMS forms. A new section type needs a template in `_includes/blocks/` and an entry here.
