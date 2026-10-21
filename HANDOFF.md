# Handoff: Noah's NYC underwriting system

Last updated 2026-10-21. Audience: an agent taking over maintenance or operation. Noah Pan is the owner; he is new to
real-estate jargon, so everything he reads must be plain sentences, and he decides pursue or pass himself.

## What it does

Noah texts an address, an ask and a strategy word (Flip, Rent or Build) to his assistant, Instinct. Instinct follows the
Underwriting Playbook, produces one Notion page per property from the Underwriting Template, and keeps one row per
building in the Properties database. A local script does the data-heavy stages from NYC Open Data when Noah runs it
himself. A separate project, `~/nyc-zr` (github.com/noah-pantastic/nyc-zr), holds the NYC Zoning Resolution as markdown with a
searchable index and a CLI; pages here cite its sections by official URL, and nothing in that project depends on this one.

## Where things live

This repo, `~/notion-underwriting` (github.com/noah-pantastic/notion-underwriting, private; `.venv/`, `.cache/` are local):

| Path | Role |
| --- | --- |
| `docs/UNDERWRITING_PLAYBOOK.md` | The instruction set Instinct follows. Source of truth; publish after editing. |
| `docs/DEAL_TEMPLATE.md` | Deal page and lighter comp page shapes, with real example links. |
| `scripts/notion_underwriting.py` | Publishes the two docs above to Notion in place (deletes blocks, re-appends). |
| `scripts/notion_deals.py` | Creates, migrates and backfills the Properties database. Idempotent; run after schema changes. |
| `scripts/screen.py` | Stages 0 to 3 for one property: Open Data pulls, envelope, flags, ACRIS comps, two maps, Notion write. |
| `scripts/notion_api.py` | Shared Notion helpers: paced `req()`, markdown to blocks, `load_state()` / `save_state()`. |
| `data/notion_state.json` | Database and page ids below. |
| `.cache/tiles` | OpenStreetMap tiles already fetched; safe to delete. |

Zoning, in `~/nyc-zr`: `python3 scripts/zr.py search|get|define|district|history` over the full Zoning Resolution text
(SQLite full-text index, built on first use from the JSONL in the repo; plain Python 3.11+, nothing to install). Use it for
any zoning question instead of fetching zr.planning.nyc.gov. Its Notion mirror was retired on 2026-10-21.

Notion, all under the "Real Estate" page `60a139f3-f569-40cf-9976-8d0c40dae1c5`:

| Page or database | Id | Notes |
| --- | --- | --- |
| Underwriting Playbook (for Instinct) | `3fa9d8ce-4a74-81e6-8885-d87cd7451488` | Published from the markdown; never hand-edit. |
| Underwriting Template v5 | `3fa9d8ce-4a74-8145-b45f-e2f540b5000c` | Same. |
| Properties database | `3fa9d8ce-4a74-8115-95f5-c286b2ef5beb` | State keys `databases.properties` and the historical `deals`. |
| Archive | `3fb9d8ce-4a74-8194-9562-faee98b3dbeb` | Old templates. Never read from it. |

Trashed: the old Comps database `3fa9d8ce-4a74-81c2-846c-c1e399a85f9c` (merged into Properties on 2026-10-16); the ZR
Sections and Definitions databases and "README for agents" (`3f99d8ce-4a74-8153-9aab-c2d09cb6ca5b`,
`3f99d8ce-4a74-8124-8759-d991c0770239`, `3fa9d8ce-4a74-8119-be68-f1820e9b355d`), retired 2026-10-21 when zoning
citations moved to the nyc-zr CLI and official URLs.

## Access

- Notion: internal integration token in `NOTION_API_TOKEN` or `NOTION_TOKEN`. Use `.venv/bin/python` and
  `scripts/notion_api.req(method, path, body, version)`; database work uses version `2022-06-28`. Never print the token.
- Google Maps Platform key: `GOOGLE_MAPS_API_KEY` in the environment for the script; Instinct keeps it in its vault as the
  login entry "Google Places API key". Optional. Never write it on a page or in a message.
- Open Data needs no key. Tiles come from tile.openstreetmap.org with a User-Agent header.
- Setup: `uv sync` (requests, matplotlib, shapely, pillow).

## Data model: the Properties database

One row per building, keyed by BBL. 27 fields. Role is Deal or Comp; a comp becomes a deal by changing Role. Strategy is
Flip, Rent, Build or Not set and gates exit comps and rents. Fields: Name, BBL, Role, Strategy, Borough, Neighborhood,
Zoning, Lot (text "17.5 × 100"), Lot sf, Existing sf, Max ZFA, Flags, Units, Building (text in words), Verdict
(Investigate / Pass / Closed by others), Noah's call (Noah only), Ask, Owner, Last sale price, Last sale date, Prior sale
(text), Sale $/sf (formula), Beds/baths, Listing URL, Comps used (self-relation; reverse "Used by"), Rules that mattered
(text: the section numbers cited on the page, "23-22, 23-344"). Anything else about a property lives on its page, not on the row. Scripts write only field
names that exist in the live schema, so deleting a field in Notion does not break them.

## Flow of one job

1. Stage 0, identify: BBL and twelve facts from PLUTO, ACRIS, DOB, HPD; links line with hyperlinked labels (Listing,
   StreetEasy, ZoLa, BIS, ACRIS, DOF); exterior photo only from a listing of this property, else Street View, else none.
2. Stage 1, envelope: max zoning floor area, height and coverage from the ZR (nyc-zr CLI), cited by official URL.
3. Stage 2, classify: unused ratio, demolition freedom, possession; strategy from Noah's word, inferred only when exactly
   one fits, otherwise Not set and the job stops after purchase comps.
4. Stage 3: area map (three pin groups: trains blue, five restaurants and cafes red, one or two large parks green; half a
   mile each way; no text in the image; colored pin list under it), ACRIS-only purchase comps with a listing pass, rents
   table from StreetEasy via Instinct's `rents-for-address` skill, exit comps by strategy.
5. Stage 4, close: three-sentence top paragraph, open items (six rows max), run log line, Research notes toggle. Never
   touch "Noah's notes" or anything below it. No returns, costs or price ladders: Noah has no cost basis yet.

`screen.py` covers stages 0 to 3 from Open Data and writes the row, comp rows and page body above "Noah's notes";
Instinct adds the photo, listing pass, rents and exit comps. Dry run: `--out $TMPDIR/x`; live: `--notion`.

## Rules that are easy to break

- The word PLUTO never appears on a page; the lot record is called ZoLa and linked to the lot's ZoLa page.
- Links are labels, never bare URLs. Template placeholders must be real URLs or Notion rejects the publish.
- Plain language: no coined words, codes spelled out, process state in database fields, not page text.
- Noah wants a discussion and an explicit go before anything changes in Notion or the scripts.
- Deleting a database field deletes its values everywhere; carry values over first (see `migrate()` for how Lot was done).
- Publishing clears the page before re-appending; a failed publish leaves it empty until re-run.

## State as of 2026-10-21

- 2026-10-21: zoning citations moved from Notion rows to the nyc-zr CLI and official zr.planning.nyc.gov URLs. The 14 deal
  rows' Rules that mattered were carried over as text and the ZR links on their pages rewritten to official URLs.
- 2026-10-17: 50 rows: 5 deals (63 Irving Place, 1241 Putnam Avenue, 324 Weirfield Street, 706 Monroe Street, 1135 Decatur Street)
  and 45 comps. 63 Irving needs a rerun under Template v5; Putnam and Decatur still show the retired new-buildings map group.
- Untested: screen.py's in-place page update path against live Notion; Google Places and Street View code (no key).
- Open with Noah: whether "projects" on the map meant NYCHA public housing; floor plan beside the photo in a two-column
  layout (proposed, not built); Condition field tied to his viewing notes (parked); cost basis and returns once he has
  contractor quotes.
- Related but separate: the iMessage showings bridge, spec at `~/showings-bridge/HANDOFF.md`.
