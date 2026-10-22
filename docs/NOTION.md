# Notion output

Where the work goes. Everything in Noah's Notion workspace is output; nothing there is instructions. All of it sits under the "Real Estate" page (`60a139f3-f569-40cf-9976-8d0c40dae1c5`). The token is an internal integration shared with that page, in the environment as `NOTION_TOKEN` (or `NOTION_API_TOKEN`), never printed and never written anywhere. Notion allows about three requests a second; `scripts/notion_api.py` paces them. Database calls use API version `2022-06-28`.

## The Properties database

https://www.notion.so/3fa9d8ce4a74811595f5c286b2ef5beb, id `3fa9d8ce-4a74-8115-95f5-c286b2ef5beb`. One row per building, keyed by BBL; the same table holds deals and comps, and a comp becomes a deal by changing Role. Find a row:

```json
POST /v1/databases/3fa9d8ce-4a74-8115-95f5-c286b2ef5beb/query
{"filter": {"property": "BBL", "rich_text": {"equals": "3019840005"}}}
```

The 27 fields. Nothing else goes on the row: lot type, unused ratio, list price, days on market, the ZoLa link and the run date live on the page.

| Field | Type | Written by | Notes |
| --- | --- | --- | --- |
| Name | title | script | the address |
| BBL | text | script | ten digits; the key |
| Role | select | script, you | Deal or Comp |
| Strategy | select | script, you | Flip, Rent, Build, Not set; never set back to Not set once set |
| Borough, Neighborhood | select | script | the neighborhood from the NTA that contains the lot |
| Zoning | multi-select | script | district, overlay, special district |
| Lot | text | script | "12.75 × 53" from lotfront and lotdepth |
| Lot sf, Existing sf, Max ZFA, Units | number | script | |
| Flags | multi-select | script, you | Historic district, Landmark, Shallow lot, Near corner, Narrow lot, Irregular lot, Rent regulated?, Open DOB violations, Open HPD violations, Active DOB job, Flood zone, City owned, Litigation, No rent history |
| Building | text | script | in words: "20 × 58 ft · 2 floors · built 1910 · three-family walk-up"; a vacant lot says "Vacant land, zoned residential" |
| Verdict | select | script, you | Investigate, Pass, Closed by others |
| Noah's call | select | Noah only | Pursue, Pass, Watch. Never set by anyone else |
| Ask | number | script | |
| Owner | text | script | |
| Last sale price, Last sale date | number, date | script | the latest ACRIS deed, $0 written as 0 |
| Prior sale | text | script | "$600,000 · December 2025" |
| Sale $/sf | formula | nobody | |
| Beds/baths | text | you | from the listing or the listing pass |
| Listing URL | url | script, you | the current listing for a deal, the sold listing for a comp |
| Comps used | relation | script, you | the deal's comp rows in this same database; the reverse side, Used by, fills itself |
| Rules that mattered | text | script, you | the section numbers cited on the page, "23-22, 23-344" |

A new deal row, `POST /v1/pages` with `"parent": {"database_id": "3fa9d8ce-4a74-8115-95f5-c286b2ef5beb"}`:

```json
{"Name": {"title": [{"text": {"content": "63 Irving Place"}}]},
 "BBL": {"rich_text": [{"text": {"content": "3019840005"}}]},
 "Role": {"select": {"name": "Deal"}}, "Strategy": {"select": {"name": "Build"}},
 "Borough": {"select": {"name": "Brooklyn"}}, "Zoning": {"multi_select": [{"name": "R6B"}]},
 "Lot": {"rich_text": [{"text": {"content": "12.75 × 53"}}]}, "Lot sf": {"number": 676}, "Max ZFA": {"number": 1352},
 "Building": {"rich_text": [{"text": {"content": "Vacant land, zoned residential"}}]},
 "Owner": {"rich_text": [{"text": {"content": "Minta Gillespie Walker Living Trust"}}]},
 "Flags": {"multi_select": [{"name": "Shallow lot"}, {"name": "Near corner"}, {"name": "Narrow lot"}]},
 "Verdict": {"select": {"name": "Investigate"}}, "Ask": {"number": 499999},
 "Comps used": {"relation": [{"id": "<page id of a comp row>"}]},
 "Rules that mattered": {"rich_text": [{"text": {"content": "23-22, 23-344"}}]},
 "Listing URL": {"url": "https://www.zillow.com/homedetails/63-Irving-Pl-Brooklyn-NY-11238/112504346_zpid/"}}
```

A comp row is the same shape with `"Role": {"select": {"name": "Comp"}}`, `"Strategy": {"select": {"name": "Not set"}}`, `"Last sale price": {"number": 625000}`, `"Last sale date": {"date": {"start": "2025-09-30"}}`, `"Prior sale": {"rich_text": [{"text": {"content": "$600,000 · December 2025"}}]}` when there is one, Beds/baths and Listing URL from the listing pass, and no Ask, Verdict or Comps used. A building that is already a Deal row is linked through Comps used and otherwise left alone.

## Writing the page

- **Links are labels.** A rich text item with a link: `{"type": "text", "text": {"content": "ZoLa", "link": {"url": "https://zola.planning.nyc.gov/l/lot/3/1984/5"}}}`. A bare URL never appears on a page.
- **Images** go through the file upload API: `POST /v1/file_uploads` with `{"mode": "single_part", "filename": "...", "content_type": "image/jpeg"}`, the bytes posted to the returned `upload_url`, then an `image` block `{"type": "file_upload", "file_upload": {"id": "..."}}`. An external URL is the fallback.
- **The pin list** under the area map is one `numbered_list_item` block per pin, its rich text colored like the pin: `"annotations": {"color": "blue"}` for trains, `"red"` for food, `"green"` for parks.
- **Research notes** is a `toggle` block titled "Research notes" with its content as children, so it opens collapsed. Never a heading.
- **"Noah's notes"** is a heading near the bottom. Nothing automated edits it or anything below it. A re-run of the script deletes and rebuilds every block above it, which also removes what was added by hand (photo, Rents, exit comps, the listing pass); add them again after a re-run.
- The "Archive" page under Real Estate holds old templates and is never read. The old instruction pages were archived on 2026-10-21.

## What the script writes

`scripts/screen.py --notion` writes the deal row (every field marked script above), one Comp row per comp building, the photo block when given `--photo`, the links line, the top paragraph, Details, Zoning, Area with the map and pin list, Purchase comps with the map and table (its Listing column empty except where DOB jobs give a renovation signal), Open items, Run log, and on a new page the "Noah's notes" heading. It never writes Pursue, never sets Strategy back to Not set, and writes only fields that exist in the live schema, so removing a field in Notion does not break it. `scripts/notion_deals.py` creates or migrates the database schema and is run only after a schema change.
