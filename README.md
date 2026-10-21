# notion-underwriting

Noah's NYC property underwriting system: the playbook his assistant (Instinct) follows, the page template it fills,
the Notion **Properties** database that holds every deal and comp, and a screening script that does the Open Data
stages on his laptop. Zoning text lives in a separate project, `~/nyc-zr`
(github.com/plloppii/nyc-zr): the NYC Zoning Resolution as searchable markdown with a CLI; pages here link to the
official section URLs.

Start with `HANDOFF.md` for the architecture, ids and rules.

## Layout

| Path | Role |
| --- | --- |
| `HANDOFF.md` | Architecture, Notion ids, data model, rules, current state. |
| `docs/UNDERWRITING_PLAYBOOK.md` | The instruction set Instinct follows. Source of truth; publish after editing. |
| `docs/DEAL_TEMPLATE.md` | Deal page and lighter comp page shapes, with real example links. |
| `scripts/notion_underwriting.py` | Publishes both docs to Notion in place. |
| `scripts/notion_deals.py` | Creates, migrates and backfills the Properties database. Idempotent. |
| `scripts/screen.py` | Stages 0 to 3 for one property from NYC Open Data, two maps, Notion write. |
| `scripts/notion_api.py` | Shared Notion helpers: paced requests, markdown to blocks, state file. |
| `data/notion_state.json` | Database and page ids (Properties, playbook, template). |

## Setup

```bash
uv sync                                   # requests, matplotlib, shapely, pillow
export NOTION_TOKEN=...                   # or NOTION_API_TOKEN; internal integration shared with the Real Estate page
export GOOGLE_MAPS_API_KEY=...            # optional: Google Places ratings and Street View photos
```

## Commands

```bash
.venv/bin/python scripts/notion_underwriting.py                         # publish playbook + template (updates in place)
.venv/bin/python scripts/notion_deals.py                                # bring the Properties database to the current schema
.venv/bin/python scripts/screen.py "63 Irving Place" --borough BK --ask 499999 --listing <url> --strategy Build --out $TMPDIR/irving   # dry run: .md + .json + two maps
.venv/bin/python scripts/screen.py --bbl 3019840005 --ask 499999 --strategy Build --notion                                            # also write the row, comp rows, page body
```

Notion pages and databases, all under Noah's "Real Estate" page:

- Playbook: https://www.notion.so/3fa9d8ce4a7481e68885d87cd7451488
- Template v5: https://www.notion.so/3fa9d8ce4a748145b45fe2f540b5000c
- Properties: https://www.notion.so/3fa9d8ce4a74811595f5c286b2ef5beb

## How it works

Strategy is Noah's word, Flip, Rent or Build, texted with the address; it is inferred only when exactly one fits (a
vacant lot is Build), otherwise the row says "Not set" and the job stops after purchase comps. A deal page opens with
the property photo, a links line and three plain sentences, then a details table, a zoning block with only the
lot-specific numbers and rules (linked to the official zr.planning.nyc.gov pages), the area map with a color-matched pin list (trains,
restaurants and cafes, large parks), a rents table from StreetEasy history, purchase comps from ACRIS deeds with a
listing pass, exit comps only with a strategy, open items, a run log, a Research notes toggle and a "Noah's notes"
heading that nothing automated edits. Returns, costs and price ladders are deliberately absent: Noah has no cost basis.

The Properties database has one row per building, keyed by BBL. Role is Deal or Comp, and a comp becomes a deal by
changing Role. The latest deed sits on the row as Last sale price and date with the one before in Prior sale; a deal
links its comps through Comps used (reverse side "Used by") and names the ZR sections it cited in Rules that
mattered (text: "23-22, 23-344"). The row holds only what is not already on the page; 27 fields as of 2026-10-17.

`screen.py` pulls PLUTO, ACRIS deeds and parties, DOB and ECB violations, BIS and DOB NOW jobs and HPD violations;
computes max zoning floor area and lot flags; finds closed same-class sales within a radius and window; renders both
maps on OpenStreetMap tiles (zoom 16, cached in `.cache/tiles`) with neighborhood outlines, a dashed half-mile frame,
a red star and numbered pins in three color groups and no text in the image; uploads the images through the Notion
file-upload API; and writes the deal row, comp rows and page body above "Noah's notes". The listing pass, rents and
exit comps are Instinct's job. Noah sets "Noah's call"; the script never writes Pursue.
