# notion-underwriting

Noah's NYC property underwriting system: the instruction set an agent follows to screen one property, the page it produces,
the Notion **Properties** database that holds every deal and comp, and the script that does the data stages. Zoning text
lives in a sibling project, `~/nyc-zr` (github.com/plloppii/nyc-zr): the NYC Zoning Resolution as searchable markdown with a
CLI; pages here link to the official section URLs.

Start with `AGENTS.md` if you are the agent doing the work, `HANDOFF.md` if you are maintaining the system. The instructions
live in this repository and nowhere else; the Notion pages that used to hold them were archived on 2026-10-21.

## Layout

| Path | Role |
| --- | --- |
| `AGENTS.md` | Entry point for any agent: what to read, the job in one screen, the four hard rules. |
| `docs/PLAYBOOK.md` | The method: rules, Stages 0 to 4, what the script does versus what the agent does by hand. Agent-neutral. |
| `docs/TEMPLATE.md` | Deal page and comp page shapes, with budgets and real example links. |
| `docs/SOURCES.md` | Every data source: the API recipes, the browser-only few, link patterns. |
| `docs/NOTION.md` | The output adapter: the Properties database, its fields and payloads, page-writing rules. |
| `docs/agents/INSTINCT.md` | Notes specific to Noah's assistant Instinct: ephemeral workspace, keys, saved routine. |
| `scripts/bootstrap.sh` | Clone or pull this repo and nyc-zr, install the packages, print a check. Idempotent. |
| `scripts/screen.py` | Stages 0 to 3 for one property: Open Data, flood maps, envelope, flags, ACRIS comps, two maps, Notion write. |
| `scripts/notion_deals.py` | Creates, migrates and backfills the Properties database. Run after schema changes only. |
| `scripts/notion_api.py` | Shared Notion helpers: paced requests, markdown to blocks, state file. |
| `data/notion_state.json` | Database ids, and the ids of the archived instruction pages. |
| `HANDOFF.md` | Architecture, ids, rules and current state, for a maintainer. |

## Setup

Python 3.10 or newer. `requests` is required; `matplotlib` and `pillow` draw the two maps and are optional (without them the
screen still runs and the page gets the pin list without the images).

```sh
sh scripts/bootstrap.sh                   # or: uv sync, or pip install -r requirements.txt
export NOTION_TOKEN=...                   # internal integration shared with the Real Estate page (NOTION_API_TOKEN also works)
export GOOGLE_MAPS_API_KEY=...            # optional: Street View photo, restaurants and cafes with ratings
python3 scripts/screen.py --check
```

## Commands

```sh
python3 scripts/screen.py "63 Irving Place" --borough BK --ask 499999 --strategy Build --listing <url> --out $TMPDIR/irving   # dry run: .md, .json, two maps
python3 scripts/screen.py --bbl 3019840005 --ask 499999 --strategy Build --notion                                            # write the row, comp rows and page body
python3 scripts/notion_deals.py                                                                                               # bring the database to the current schema
```

Notion, under Noah's "Real Estate" page: the Properties database is https://www.notion.so/3fa9d8ce4a74811595f5c286b2ef5beb.

## How it works

Noah sends an address, an ask and a strategy word (Flip, Rent or Build). The agent bootstraps a workspace, runs the screen,
and finishes by hand what no API reaches: the photo, the listing's facts, the tax bill, the listing pass on each comp, rents
and exit comps. Strategy is inferred only when exactly one fits (a vacant lot is Build); otherwise the row says "Not set" and
the job stops after purchase comps. A deal page opens with the property photo, a links line and three plain sentences, then a
details table, a zoning block with only the lot-specific rules (linked to the official zr.planning.nyc.gov pages), the area
map with a color-matched pin list, a rents table from StreetEasy history, purchase comps from ACRIS deeds with a listing pass,
exit comps only with a strategy, open items, a run log, a Research notes toggle and a "Noah's notes" heading that nothing
automated edits. Returns, costs and price ladders are deliberately absent: Noah has no cost basis yet.

The Properties database has one row per building, keyed by BBL. Role is Deal or Comp, and a comp becomes a deal by changing
Role. The latest deed sits on the row as Last sale price and date with the one before in Prior sale; a deal links its comps
through Comps used and names the ZR sections it cited in Rules that mattered. The row holds only what is not already on the
page; 27 fields as of 2026-10-17.

`screen.py` pulls PLUTO, ACRIS deeds and parties, DOB and ECB violations, BIS and DOB NOW jobs and HPD violations, and the
flood zone from FEMA's effective maps and the city's copy of the 2015 preliminary maps (both ArcGIS REST, no key); computes
max zoning floor area and lot flags; finds closed same-class sales within a radius and window; renders both maps on
OpenStreetMap tiles (cached in `.cache/tiles`) with neighborhood outlines, a dashed half-mile frame, a red star and numbered
pins in three color groups and no text in the image; uploads the images through the Notion file-upload API; and writes the
deal row, comp rows and page body above "Noah's notes". It never writes Pursue.
