# Lab 07 — Publish Workflow And Site Tree

## Goal

Bring the weather CMS together: review the page tree, practice draft vs live, and confirm the public site matches editorial intent.

## Time

45 minutes

## Learning Outcomes

By the end of this lab, participants can:

- Navigate and explain the Wagtail page tree for the weather app
- Use draft and publish correctly
- Unpublish or update warnings safely
- Describe a minimal go-live checklist for this training site

## Background

Wagtail separates **saving** from **publishing**. Duty officers can prepare a warning draft before it is public.

Your target tree by now:

```text
Root
└── Home (HomePage)
    ├── Warnings (WarningIndexPage)
    │   ├── Warning A (WarningPage)
    │   └── Warning B (WarningPage)
    └── Public Forecast — … (ForecastPage)
```

Snippets (stations) live outside this tree.

## Task 1: Map Your Tree

In admin → **Pages**, sketch your actual tree.

Answer:

1. Which pages are live right now?
2. Which page is the site homepage (Site settings → default site root / welcome page)?
3. Does every `WarningPage` sit under the index?

Fix any misplaced pages before continuing.

## Task 2: Draft vs Live Warning

1. Create a new warning titled `DRAFT ONLY — Training`
2. Fill required fields
3. **Save draft** (do not publish)
4. Visit the warnings index on the public site

Answer:

1. Does the draft appear in `page.get_children.live`?
2. Who can still see the draft, and where?
3. Why does this matter for real severe-weather messaging?

Publish the page, refresh the index, then **unpublish** it and confirm it disappears from the public list.

## Task 3: Homepage Sanity Check

Visit `/` and confirm:

- [ ] Title and hero text show
- [ ] Intro rich text shows
- [ ] Hero image shows (if set in Lab 04)
- [ ] Navigation or links can reach Warnings and a Forecast (add simple links in intro or template if needed)

If links are missing, add a short “Find warnings” link in the homepage intro pointing at `/warnings/` (or your index slug).

## Task 4: Go-Live Checklist (Training)

Write a short checklist (5–8 bullets) your team would run before calling the training site “ready for demo,” covering:

- migrations applied
- superuser available
- at least one live warning and one forecast
- image uploaded
- stations snippet populated
- parent/child rules preventing bad trees

## Questions

1. What is the difference between delete and unpublish?
2. Why should severe warnings not rely on unpublished drafts for public safety messaging?
3. If two editors edit the same warning, what process would you want in a real MET office? (Opinion — no single code answer.)

## Checkpoint

You have finished Wagtail Essentials for this weather app when you can:

- Explain the page tree and snippet boundary
- Publish and unpublish confidently
- Point to models, templates, and migrations for each content type you built

## Stretch (Optional)

- Add a simple “Latest warnings” list on `HomePage` using `WarningIndexPage` children
- Add basic CSS in `app/static/css/app.css` for severity badges
- Document your final model list in team notes for a follow-on Postgres lab
