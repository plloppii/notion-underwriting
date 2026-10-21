# Handoff: Noah's NYC underwriting system

Last updated 2026-10-21. Audience: an agent or person taking over maintenance. Noah Pan is the owner; he is new to real-estate
jargon, so everything he reads must be plain sentences, and he decides pursue or pass himself.

## What it does

Noah texts an address, an ask and a strategy word (Flip, Rent or Build) to his assistant, Instinct. The agent follows the
instructions in this repository (read from a fresh clone every job, since its workspace is not persistent), runs
`scripts/screen.py` for the data stages, finishes the page by hand, and keeps one row per building in the Notion Properties
database. A separate project, `~/nyc-zr` (github.com/plloppii/nyc-zr), holds the NYC Zoning Resolution as markdown with a
searchable index and a CLI; pages here cite its sections by official URL, and nothing in that project depends on this one.

## Where things live

This repo, `~/notion-underwriting` (github.com/plloppii/notion-underwriting, private; Instinct has read access and clones it;
`.venv/`, `.cache/` are local):

| Path | Role |
| --- | --- |
| `AGENTS.md` | Entry point for any agent: reading order, the job in one screen, the four hard rules. |
| `docs/PLAYBOOK.md` | The method, agent-neutral. Section 1 has the division of labor between the script and the agent. |
| `docs/TEMPLATE.md` | Deal page and comp page shapes, with the budgets table at the end. |
| `docs/SOURCES.md` | Every data source with its API recipe, the browser-only few, link patterns. |
| `docs/NOTION.md` | The Properties database (27 fields, payloads) and the page-writing rules. The only Notion-specific document. |
| `docs/agents/INSTINCT.md` | What is specific to Instinct: ephemeral workspace, Python 3.10, vault key, saved routine rents-for-address. A new agent gets its own file here. |
| `scripts/bootstrap.sh` | Clone or pull both repos under `$UW_HOME` (default `$HOME`), pip install, `screen.py --check`, zr tool check. Idempotent. |
| `scripts/screen.py` | Stages 0 to 3: Open Data pulls, flood zone from two map services, envelope, flags, ACRIS comps, two maps, Notion write. Python 3.10+. |
| `scripts/notion_deals.py` | Creates, migrates and backfills the Properties database. Idempotent; run after schema changes. |
| `scripts/notion_api.py` | Shared Notion helpers: paced `req()`, markdown to blocks, `load_state()` / `save_state()`. |
| `data/notion_state.json` | Database ids; the two archived instruction pages under `pages_archived`. |
| `.cache/` | OpenStreetMap tiles and matplotlib's cache; safe to delete. |

Zoning, in `~/nyc-zr`: `python3 scripts/zr.py search|get|define|district|history` over the full Zoning Resolution text
(SQLite full-text index, built on first use from the JSONL in the repo; plain Python, nothing to install; verified on 3.10 on
2026-10-21). Use it for any zoning question instead of fetching zr.planning.nyc.gov. Its Notion mirror was retired on 2026-10-21.

Notion, all under the "Real Estate" page `60a139f3-f569-40cf-9976-8d0c40dae1c5`:

| Page or database | Id | Notes |
| --- | --- | --- |
| Properties database | `3fa9d8ce-4a74-8115-95f5-c286b2ef5beb` | State keys `databases.properties` and the historical `deals`. |
| Archive | `3fb9d8ce-4a74-8194-9562-faee98b3dbeb` | Old templates. Never read from it. |

Archived (in Notion's trash, restorable): "Underwriting Playbook (for Instinct)" `3fa9d8ce-4a74-81e6-8885-d87cd7451488` and
"Underwriting Template v5" `3fa9d8ce-4a74-8145-b45f-e2f540b5000c`, on 2026-10-21 when the instructions moved here for good; the
old Comps database `3fa9d8ce-4a74-81c2-846c-c1e399a85f9c` (merged into Properties on 2026-10-16); the ZR Sections and
Definitions databases and "README for agents" (`3f99d8ce-4a74-8153-9aab-c2d09cb6ca5b`, `3f99d8ce-4a74-8124-8759-d991c0770239`,
`3fa9d8ce-4a74-8119-be68-f1820e9b355d`), retired 2026-10-21.

## Access

- Notion: internal integration token in `NOTION_API_TOKEN` or `NOTION_TOKEN`. `scripts/notion_api.req(method, path, body,
  version)`; database work uses version `2022-06-28`. Never print the token.
- Google Maps Platform key: `GOOGLE_MAPS_API_KEY` in the environment for the script; Instinct keeps it in its vault as the
  login entry "Google Places API key". Optional. Never write it on a page or in a message.
- GitHub: github.com/plloppii/notion-underwriting, Noah's personal account (SSH alias `github-personal`; never the work account).
  Instinct has read access and clones over HTTPS.
- Open Data needs no key. Neither do the two flood map services: FEMA's National Flood Hazard Layer (hazards.fema.gov, ArcGIS
  REST layer 28, the effective maps that set insurance; the host resets some connections, so the script retries) and NYC
  Emergency Management's copy of the 2015 preliminary maps (services1.arcgis.com, PFIRM layer 0, what the Building Code uses for
  new construction). Tiles come from tile.openstreetmap.org with a User-Agent header.
- Python: 3.10 or newer. `requests` required; `matplotlib` and `pillow` optional (maps). Shapely was dropped on 2026-10-21 in
  favor of a few lines of GeoJSON math (`_rings`, `contains`, `rep_point` in screen.py). `uv sync`, `pip install -r
  requirements.txt` or `sh scripts/bootstrap.sh`.

## Data model: the Properties database

One row per building, keyed by BBL. 27 fields, listed with types and who writes each in `docs/NOTION.md`. Role is Deal or Comp;
a comp becomes a deal by changing Role. Strategy is Flip, Rent, Build or Not set and gates exit comps and rents. Anything else
about a property lives on its page, not on the row. Scripts write only field names that exist in the live schema, so deleting a
field in Notion does not break them.

## Flow of one job

1. Bootstrap: clone if missing, `sh scripts/bootstrap.sh` (pull both repos, install, check).
2. `python3 scripts/screen.py "<address>" --borough BK --ask <n> --strategy <word> --listing <url> --notion`: Stage 0 facts
   (PLUTO, ACRIS, DOB, ECB, HPD, the two flood maps, E-designation), Stage 1 envelope and flags with ZR citations, Stage 2
   classifiers and strategy inference, Stage 3 area map with pin list and ACRIS-only purchase comps with comp rows, a draft
   top paragraph, open items and run log; the row and page body are written above "Noah's notes".
3. By hand: photo and floor plan from the listing, the listing's facts, the DOF tax bill row, HPD registration when units are in
   question, the listing pass on each comp (Listing column, Beds/baths and Listing URL on comp rows), the Rents table, exit
   comps by strategy, then sentences 1 and 3 of the top paragraph, the final open items, Rules that mattered, a Run log line.
4. Never touch "Noah's notes" or anything below it. No returns, costs or price ladders.

A re-run of the script rebuilds everything above "Noah's notes" and drops the hand-added parts; the playbook tells the agent to
re-run only when facts or comps need refreshing.

## Rules that are easy to break

- The word PLUTO never appears on a page; the lot record is called ZoLa and linked to the lot's ZoLa page.
- Links are labels, never bare URLs. Template placeholders must be real URLs or Notion rejects the publish.
- Plain language: no coined words, codes spelled out, process state in database fields, not page text.
- Noah wants a discussion and an explicit go before anything changes in Notion or the scripts.
- Deleting a database field deletes its values everywhere; carry values over first (see `migrate()` for how Lot was done).
- The instructions live in this repo, not Notion, and the four documents under `docs/` are agent-neutral: anything specific to
  one agent goes in `docs/agents/`. Edit the markdown, commit, push; the agent picks it up on its next bootstrap.

## State as of 2026-10-21

- 2026-10-21 (later): the script is the default path for the agent; docs split into AGENTS.md plus PLAYBOOK, TEMPLATE, SOURCES,
  NOTION and agents/INSTINCT; the two Notion instruction pages archived and `scripts/notion_underwriting.py` (which kept them)
  removed; Python 3.10 supported and verified by dry runs with the full dependency set and with `requests` alone; shapely
  dropped; `bootstrap.sh` and `screen.py --check` added.
- 2026-10-21: instructions moved to GitHub. Flood zone comes from FEMA's effective maps and the city's 2015 preliminary maps by
  API (`flood_zone()` in screen.py, SOURCES.md); the Flood Hazard Mapper is no longer used.
- 2026-10-21: zoning citations moved from Notion rows to the nyc-zr CLI and official zr.planning.nyc.gov URLs. The 14 deal
  rows' Rules that mattered were carried over as text and the ZR links on their pages rewritten to official URLs.
- 2026-10-17: 50 rows: 5 deals (63 Irving Place, 1241 Putnam Avenue, 324 Weirfield Street, 706 Monroe Street, 1135 Decatur Street)
  and 45 comps. 63 Irving needs a rerun under Template v5; Putnam and Decatur still show the retired new-buildings map group.
- Untested: `bootstrap.sh` on a real fresh agent sandbox (verified here only against local clones); screen.py's in-place page
  update path against live Notion; Google Places and Street View code (no key); the Flood row and flag on a live Notion page
  (dry runs verified them for 85 Dikeman Street, zone AE on both maps, 10 ft effective and 12 ft preliminary).
- Open with Noah: whether "projects" on the map meant NYCHA public housing; floor plan beside the photo in a two-column layout
  (proposed, not built); Condition field tied to his viewing notes (parked); cost basis and returns once he has contractor
  quotes; adding the DOF assessment dataset (`yjxr-fw8i`) and HPD registrations (`tesw-yqqr`) to the script.
- Related but separate: the iMessage showings bridge, spec at `~/showings-bridge/HANDOFF.md`.
