# Underwriting playbook (for Instinct)

Read this page at the start of every underwriting job. It is instructions for you, not content. Never copy any of it onto a property page. The page follows the "Underwriting Template v5" page exactly. Revised 2026-10-16; Noah owns the defaults in section 7.

## 0. Rules that override everything

1. A property page holds facts, numbers, maps and a verdict. This page holds the method. No methodology, definitions, formulas, source recipes or process text on a property page.
2. The word budgets in the template win. There are no Status tags. The Source column carries provenance; an estimate says so inside the Finding in five words or fewer ("about 63 ft, survey to confirm"). A caveat that does not fit is dropped or goes to Research notes.
3. A zoning rule on a page is at most three lines: one plain-English sentence, the number for this lot, what proves it, and the link to the rule's row in the Notion ZR Sections database (never the zr.planning.nyc.gov URL; the row carries it). The quoted text and anything longer go under a collapsed toggle named "Research notes" near the bottom of the page, which has no budget. Rules that apply to every lot in the district (height, coverage, standard yards, density) are not written on property pages.
4. A blank is Unknown, not zero. Never invent rents, costs, cap rates, zoning bonuses or legal vacancy. Leave Unknown and add an open item.
5. Asking price is not a closed price. Tax or PLUTO area is not legal area. An asking rent from a past listing is not a rent roll. Existing is not proposed. An estimate is not an approval. Record a conflict as two numbers, each with its source; never average them.
6. Only sections that apply go on the page. Omit the rest and do not explain the omission. No placeholder text such as "pending", "provisional" or "not checked": a section either has content or is absent.
7. Do not contact brokers, lenders, tenants or sellers, order paid reports, submit financing or make offers.
8. Stop only at a hard gate: no lawful path to the use, possession legally blocked, or title that cannot close. Whether the price is good enough is Noah's decision, never yours. You do not compute returns, profit or a price ladder; that part of the process is not built yet.
9. Nothing on a page is for Noah to fill in. His only input is the "Noah's call" property on the row. Never write notes addressed to Noah or to yourself on the page, and never edit the "Noah's notes" heading or anything below it.
10. The strategy comes from Noah: Flip, Rent or Build (section 4). Infer one only when exactly one fits the facts. Otherwise the row's Strategy stays "Not set" and the job ends after purchase comps.
11. Links are labels. A bare URL never appears on a page. The links line reads "Listing · StreetEasy · ZoLa · BIS · ACRIS · DOF", each word a link (`{"type": "text", "text": {"content": "ZoLa", "link": {"url": "https://zola.planning.nyc.gov/l/lot/3/3428/54"}}}`), and every source name in a table links the same way to the lot-specific page (section 2, Links). On the page the city's lot record is called ZoLa, the map that displays it; the word PLUTO is the dataset name for your queries and never appears on a page.

## 1. Trigger, scope and dedupe

- Trigger: Noah texts an address and borough, usually with a strategy word (Flip, Rent, Build), the asking price and a listing link. One property per job.
- Resolve the BBL first (Stage 0, fact 1). Then query the Properties database by BBL (section 8). A row with Role Comp becomes the deal: set Role to Deal and fill its page the rest of the way. A row with Role Deal is updated in place above "Noah's notes", with a line added to its Run log. No row: create one with Role Deal and the body from the template. Never create a second row for the same BBL.
- Scope of every job: Stages 0 to 3 and the top paragraph. Exit comps and the rents work that depends on a strategy run only when Strategy is set. Nothing about returns, costs or price ladders.
- A later text about the same property re-runs only the stages it touches.
- "rents for <address>" on its own runs your saved routine rents-for-address and answers in chat; nothing is written to Notion for that.

## 2. Stage 0: Identify

Twelve facts, one lookup each. All NYC Open Data calls are `GET https://data.cityofnewyork.us/resource/<dataset>.json` with SoQL parameters; no token is needed for this volume. Null fields are omitted from the JSON, so a missing key means "not set", not an error. Example values use 63 Irving Place (BBL 3019840005) and 130 Greene Avenue (BBL 3019610038).

| # | Fact | Source | Recipe |
| --- | --- | --- | --- |
| 1 | BBL, block, lot, lat/long, lot front and depth, lot area, lot type | PLUTO `64uk-42ks` | `$where=upper(address)='63 IRVING PLACE' AND borough='BK'` or `$where=bbl=3019840005`. Boroughs: MN BX BK QN SI. Fields: bbl, block, lot, lotarea, lotfront, lotdepth, lottype (3 corner, 4 through, 5 interior), irrlotcode, latitude, longitude, version |
| 2 | Zoning district, overlay, special district | PLUTO zonedist1-4, overlay1-2, spdist1-3, splitzone; confirm on ZoLa | ZoLa lot URL: `https://zola.planning.nyc.gov/l/lot/<boro 1-5>/<block>/<lot>` |
| 3 | Historic district or landmark | PLUTO histdist, landmark | Absent keys mean none. Example: 130 Greene has `histdist = Clinton Hill Historic District` |
| 4 | Existing building: class, year, floors, units, gross area, built FAR, footprint | PLUTO bldgclass, yearbuilt, numfloors, unitsres, unitstotal, bldgarea, builtfar, numbldgs, bldgfront, bldgdepth | Class families: A one-family, B two-family, C walk-up (C0 three-family, C3 four-family, C1/C2/C4-C7 larger), S mixed residential with store, D elevator, R condo units, V0 vacant residential land. bldgarea is DOF gross area, its own basis. Write classes in words on the page |
| 5 | Maximum residential FAR | PLUTO residfar; the rule is ZR 23-22 (R6 to R12) or 23-21 (R1 to R5) | Read the rule from the Notion Sections database with filter Section ID equals "23-22". Column 2 of the 23-22 table (qualifying affordable housing) is upside, not base |
| 6 | Owner and last deed | ACRIS on Open Data: legals `8h5j-fqxa`, master `bnx9-e6tj`, parties `636b-3b5g` | Legals: `$where=borough='3' AND block='1984' AND lot='5'` gives document_id values. Master: `$where=document_id in ('id1','id2') AND doc_type='DEED'` gives document_date and document_amt. Parties: by document_id, party_type 1 seller, 2 buyer. document_amt under 100000 is not a market sale. ACRIS UI for links: `https://a836-acris.nyc.gov/bblsearch/bblsearch.asp?borough=3&block=1984&lot=5`. Document images return 403 to you; link, do not read |
| 7 | BIN | PAD `bc8t-ecyu` by bbl, or any DOB filing below | BIS profile for links: `https://a810-bisweb.nyc.gov/bisweb/PropertyProfileOverviewServlet?bin=<bin>` |
| 8 | DOB and ECB violations | DOB `3h2n-5cm9`, ECB `6bgk-3dad` | DOB: `$where=boro='3' AND block='01961' AND lot='00038'` (block 5 digits, lot 5 digits, zero padded). ECB: `$where=boro='3' AND block='01961' AND lot='0038'` (lot 4 digits). Count open versus dismissed from violation_category and ecb_violation_status; sum balance_due |
| 9 | DOB jobs, both systems | BIS jobs `ic3t-wcy2`, DOB NOW `w9ak-ipjd` | BIS: `$where=bbl='3019610038'`; fields job__, job_type (NB, A1, A2, A3, DM), job_status_descrp, pre__filing_date, proposed_dwelling_units, proposed_zoning_sqft. DOB NOW: `$where=bbl='3019610038'`; fields job_filing_number, job_type, filing_status, filing_date, proposed_dwelling_units, total_construction_floor_area, approved_date, signoff_date |
| 10 | HPD violations and registration | HPD `wvxf-dwi5` | `$where=bbl='3019610038' AND violationstatus='Open'`; count by class A, B, C. HPD Online for registration and I-cards when units are in question |
| 11 | Taxes, exemptions, rent-regulation signal | DOF Property Information Portal | `https://propertyinformationportal.nyc.gov/parcels/parcel/<bbl>`. Record annual bill, exemptions and arrears. A "Rent Stabilization" fee line on the bill is the best public signal that units are regulated. The HCR building list is a lead, not proof, in both directions |
| 12 | Flood and environmental | NYC Flood Hazard Mapper; PLUTO has no flood field | Record the zone or "none mapped" |

Also capture from the listing Noah sent, all tagged Broker: asking price, marketed area, beds and baths, floor plan, photos, days on market, stated taxes and rents.

Links, for the links line and for every Source cell, all lot-specific: Listing, the live listing Noah sent (no listing: the label is "Off market", linked to the property's Zillow or StreetEasy page); StreetEasy, the building page `https://streeteasy.com/building/<house>-<street>-<borough>` (open it to confirm it loads; omit the item if it does not); ZoLa, `https://zola.planning.nyc.gov/l/lot/<boro>/<block>/<lot>`; BIS, the property profile by BIN; ACRIS, `https://a836-acris.nyc.gov/bblsearch/bblsearch.asp?borough=<boro>&block=<block>&lot=<lot>`; DOF, `https://propertyinformationportal.nyc.gov/parcels/parcel/<bbl>`; HPD, `https://hpdonline.nyc.gov/hpdonline/building/search-results?...` or the building page you reached. Never the generic search pages.

Photo: the first block of the page is a picture of the front of this property. It comes only from a listing of this property, live or sold: open it in your browser, save the lead exterior photo as a file and upload it with the Notion file upload API, so it survives the listing going down. An off-market page is not a listing. An image that does not show this building's exterior, or that carries any text, logo or advertising, is not a photo: skip it. A floor plan, when the listing has one, goes the same way: scroll to it, crop the screenshot, upload it under the Floor plan heading. If there is no listing or no usable photo, use Google Street View with the key from your vault (section 8): `GET https://maps.googleapis.com/maps/api/streetview/metadata?location=<lat>,<lon>&key=<key>` and continue only when status is OK, then `GET https://maps.googleapis.com/maps/api/streetview?size=640x400&location=<lat>,<lon>&fov=70&key=<key>`, uploaded the same way. If neither works, the links line begins "No photo · ". Never write the key on a page.

## 3. Stage 1: Envelope

Formulas, with the citation to put on the page:

- Max zoning floor area (ZFA) = lot area × residfar. Cite ZR 23-22 or 23-21. Carry the affordable-housing FAR as an upside line only when the lot could plausibly take 5 or more units.
- Unused rights = max ZFA minus PLUTO bldgarea. Screen only: bldgarea is gross and includes space that is not zoning floor area.
- Unused ratio U = bldgarea ÷ max ZFA. Vacant lot: U = 0.
- Height: ZR 23-432 table for R6 to R12 (R6B: base 30 to 45 ft, maximum 55 ft standard, 65 ft with qualifying affordable housing); 23-42 series for R1 to R5.
- Coverage: ZR 23-362 for R6 to R12 (80 percent interior or through, 100 percent corner); 23-361 for R1 to R5.
- Rear yard: ZR 23-342 (30 ft standard). Side yards R6 to R12: 23-335. Front yards R6 to R12: 23-322. Lot area and width minimums R6 to R12: 23-12 (1,700 sf and 18 ft for most residences). Density: 23-52.
- Flags, set from PLUTO geometry and checked on ZoLa: Corner (lottype 3). Through (lottype 4). Shallow (lotdepth under 95 ft, ZR 23-342(b) candidate, 1961 history must be proven). Near corner (any part within 100 ft of a street intersection, ZR 23-344(a) no rear yard and 23-363(b) full coverage candidate; the survey decides). Narrow or small (lotfront under 18 ft or lotarea under 1,700 sf, below the 23-12 minimums; ZR 23-10 exempts a zoning lot that existed on December 5, 2024 and has not shrunk since, so this is a one-line Zoning entry, not a gate). Irregular (irrlotcode true, do not use front × depth).

To read a rule, use the Notion Sections database with the filter Section ID equals "23-344" as described in "README for agents". Link that row on the page; the official URL is on the row for anyone who wants it. Quote the operative sentence only in Research notes.

Output on the page: the Zoning block, lot-specific numbers only, with one entry of up to three lines per rule that applies to this lot. Flags are never listed as tags on the page; each one becomes a finding in words or a Zoning entry.

Gate: hard blocks only. If the intended use is not permitted, possession is legally blocked, or title cannot close, start the top paragraph with "Pass:" and the reason, set Verdict to Pass on the row, and stop. If U is at least 0.8 and the units are occupied and regulated and the building is in a historic district, say so in the top paragraph (income only) and continue; the price call is Noah's.

## 4. Stage 2: Classify, then strategy

Three classifiers describe what the property allows. Compute them; they shape sentence 1 of the top paragraph and the price basis of the comps. There is no field for them on the row.

| Classifier | Value | Meaning |
| --- | --- | --- |
| A. Unused ratio U | 0, or under 0.4 | Development or enlargement site |
| | 0.4 to 0.8 | Enlargement possible (add floors, rear extension); economics are renovation |
| | over 0.8 | Renovation or income; land value is irrelevant |
| B. Demolition freedom | histdist or landmark set | No demolition, LPC review on exterior work; development only if the lot is vacant |
| | neither set | Demolition and new building are options |
| C. Possession | unitsres over 0 and any of: rent-stabilization fee on the tax bill, HCR hit, 6 or more units built before 1974 | Income in place; lawful rents, no vacancy assumption |
| | otherwise | Vacant or free-market delivery plausible; confirm with listing and leases |

Say what classifier A means in sentence 1, in words: a development site, a building with room to grow, a renovation, or an income building with tenants in place. Land is priced per buildable sf; a building per sf.

Product by size, when the lot can be built on: ZFA under 2,500 sf is a one- or two-family house. 2,500 to 6,000 sf is a two- to four-family. Over 6,000 sf or 5 or more units is a small condo or rental building, which brings elevator, egress and 23-52 density questions.

Strategy is what Noah intends to do. It comes from his text and goes on the row.

| Strategy | Meaning | Exit evidence (section 5) |
| --- | --- | --- |
| Flip | Buy as-is, renovate, sell | Exit comps: closed sales whose listing text says renovated, gut renovated or new |
| Rent | Buy, renovate as needed, hold | Rents table for the building, and the rents of renovated comps |
| Build | Vacant or badly underbuilt lot (U under 0.4, no landmark), new construction | Exit comps: land sales per buildable sf and new-construction sales |

If Noah did not name one: a vacant lot is Build; an occupied building with regulated tenants is Rent; anything else is "Not set". With "Not set" the job ends after purchase comps and the row says so; the page carries no note about it.

Top paragraph format: three sentences of plain prose with no labels, directly under the links line. Sentence 1: "Investigate:" or "Pass:" then what it is and, when the strategy is set, what the strategy would make of it. Sentence 2: the ask against the best analog per buildable sf (per sf for a building). Sentence 3: the fact that decides it. Example: "Investigate: vacant 12.75 × 53 ft R6B interior lot in Clinton Hill that builds a 1,352 sf one- or two-family house. The ask is $370 per buildable sf; the one R6B lot of similar size sold at $223. A survey showing the lot sits within 100 ft of the Putnam corner removes the rear yard; failing that, the 1961 lot depth gives a 10 ft yard." Verdict words you may write, on the row and in sentence 1: Pass means a hard gate blocks every path; Investigate means a path exists and the fact in sentence 3 decides it. Pursue is written only by Noah in "Noah's call". Do not rank, recommend or grade the deal beyond that.

## 5. Stage 3: Area, comps and rents

Comp rules: closed within 18 months, within half a mile, same product family. Purchase comps are as-is sales: a sale whose listing says renovated, gut renovated or new is an exit comp and never sits in the purchase table (with Strategy "Not set" it is left out; name it in the sentence only when it is the same lot as a purchase comp). Widen distance or time only when needed and say so in the sentence under the table. Listings and in-contract deals are asks, not comps; they get a hollow pin and their row has no Last sale. The table has exactly the template's columns: #, Address (the address linked to its ACRIS page, then the distance), Closed, Price, Zoning, Area · basis ("2,430 sf · building", "5,000 sf · buildable" or "marketed"), $/sf, Listing ("$1.25M list · 41 days · [link]" or "not listed"; beds, baths and condition words go on the row, not in this cell).

Closed sales come from ACRIS deeds only. Do not use the Department of Finance rolling sales file or any other sales list: every closed comp on every page is a recorded deed, so comps are comparable across pages.

Closed-sale recipe on Open Data:

1. Candidate lots: PLUTO `$where=latitude between 40.676 and 40.690 AND longitude between -73.968 and -73.950 AND bldgclass like 'V%'` for land, or `like 'A%'`, `'B%'`, `'C%'` for houses and walk-ups. Keep bbl, block, lot, address, lotarea, bldgarea, residfar, unitsres.
2. Deeds: ACRIS legals `$where=borough='3' AND block in ('1983','1984') AND good_through_date >= '2024-01-01T00:00:00.000'` gives document_id per lot. Master `$where=document_id in (...) AND doc_type='DEED' AND document_date >= '2025-04-01T00:00:00.000' AND document_amt > 100000` gives price and date.
3. Join back to PLUTO by block and lot for area and class. Price basis: land is price ÷ (lotarea × residfar), stated as $/buildable sf. Houses are price ÷ bldgarea, stated as $/PLUTO sf, unless a marketed area is known and labeled. Five or more units: $/unit.
4. Listing pass, once per closed comp: find the sold listing on Redfin first, then Zillow, then Compass. Record beds and baths and the listing URL on the comp's row (Beds/baths, Listing URL); list price and days on market go only in the table's Listing column as "$1.25M list · 41 days · [link]". Nothing on any of the three: write "not listed", which usually means an off-market sale. One lookup per comp, a few seconds apart, and never more than the eight comps on the page. A comp whose row already has a Listing URL was found in an earlier job: open that URL for the list price and days instead of searching again. If a site rate-limits you, stop using that site for the rest of the job and note it in the Run log line.

Every comp is a row in the Properties database with Role Comp, one row per building, keyed by BBL. The latest sale goes on the row as Last sale price and Last sale date; the sale before it goes in Prior sale as "$600,000 · December 2025". Two sales within three years are a renovation pair; name it in the sentence under the table. Reuse an existing row rather than creating a second one for the same BBL; if the BBL is already a Deal row, link it without changing it. Link the deal to its comps through "Comps used" (the reverse side, "Used by", fills itself). A comp's page is the light version of the template (comp page, in the template): photo from the sold listing, links line, one or two sentences on what it is, what it sold for and what the listing said about its condition, a details table of at most five rows, the Rents table if StreetEasy has history, and the Noah's notes heading. No maps, no zoning block, no comps of its own. A tracked deal that records a deed later is the same row: set Last sale price and date, Verdict to Closed by others.

Exit comps, only when Strategy is set, same table shape, up to eight rows, one sentence: Flip takes closed sales whose listing text says renovated, gut renovated or new; Rent takes renovated comps and reports their rents; Build takes land sales per buildable sf and new-construction sales. Purchase comps stay what they were: as-is sales of the same product family.

Rents, whenever the building has units: run your saved routine rents-for-address for the subject and put the result on the page under a "Rents" heading as a table, one row per unit: Unit, Beds/baths, Last asking rent, Listed (month and year), StreetEasy: the label "unit page" linked to that unit's page, or "building page" linked to the building when the unit has no page of its own. The column header says asking rent: these are asking rents from past listings, not a rent roll, and the actual rents stay an open item resolved by leases. When StreetEasy has no history for the building, the section is absent and the row's Flags gets "No rent history". For Rent strategy, also run the routine for each renovated exit comp, put its table on that comp's page, and cite the rent per unit in the exit-comps sentence.

Area map spec:

- Frame: the square that runs half a mile west to half a mile east and half a mile north to half a mile south of the subject, so one mile on a side. The image covers that frame plus about 8 percent of margin on each side and nothing more; never zoom out to bring a pin into view. A pin outside the frame is not drawn; when a group has nothing inside the frame, one list line says so with the nearest one and its distance ("No subway station inside the frame; nearest Wilson Av (L) 0.26 mi").
- Basemap: OpenStreetMap street tiles at zoom 16 (`https://tile.openstreetmap.org/16/{x}/{y}.png`, one request per tile, with a User-Agent header), stitched and cropped to the frame, north up. Over the tiles draw the city's 2020 neighborhood boundaries from `9nt8-h7nd` as thin plum outlines (the tile labels already name the neighborhoods), the half-mile frame as a dashed square, and the subject as a red star.
- Three groups of pins, numbered in one sequence in this order, each group one color: trains in blue, every subway station inside the frame, from `https://data.ny.gov/resource/39hk-dx4f.json` (gtfs_latitude, gtfs_longitude, stop_name, daytime_routes); food in red, the top five restaurants and cafes by rating weighted by review count, from Google Places (New), `POST https://places.googleapis.com/v1/places:searchNearby` with the key from your vault in the `X-Goog-Api-Key` header, includedTypes restaurant, cafe, bakery, a 800 m circle, each line carrying its rating and rating count (without the key: OpenStreetMap through your browser, since overpass-api.de refuses direct requests, amenity cafe, restaurant or bakery, the five nearest, no ratings, and the caption says "cafes and restaurants: OpenStreetMap, no ratings"); parks in green, the two largest inside the frame of at least one acre from `enfh-gkve`, or the single largest when none reaches an acre. About ten pins. No schools, no new-building or construction projects, nothing else. No title, legend, labels or any other text in the image.
- Under the image, in this order: one caption line naming the sources and the checked date and including "© OpenStreetMap contributors"; the pin list as Notion numbered-list blocks in pin order, grouped by type, each line's text colored to match its pins; this is required, not optional: every block's rich_text item carries `"annotations": {"color": "blue"}` for trains, `"red"` for food, `"green"` for parks, such as "Halsey St (L) · subway · 0.20 mi" or "Saraghina · restaurant · 4.6 (1,200 ratings) · 0.15 mi"; then one sentence only for a negative (historic district, flood zone). Nothing on development pace or nearby filings. A layer that fails gets one clause at the end of the caption ("cafes and restaurants: source unreachable"), never a paragraph. Keep the map code in the Research notes toggle as a code block so the next run can reuse it.

Comps map spec: same basemap, frame and star. Comps are numbered in the order of the table, dark filled pin for a closed sale, hollow pin for a listing or in-contract. No text in the image; the table is the legend. The table below the map lists every qualifying comp, up to eight rows, nearest first, with each comp's zoning district and the Listing column from the listing pass. One sentence follows it naming the best analogs (same district as the subject, one-third to three times its size) against the ask. No implied-value range.

Images: upload with the Notion file upload API (`POST /v1/file_uploads`, send the bytes, then an `image` block with the `file_upload` id), or attach an external URL.

## 6. Stage 4: Close

- Finish the top paragraph: three sentences, the third naming the one fact that decides the deal.
- Open items table, at most six rows: Missing fact, how it moves the deal, evidence needed, who resolves it. Actual rents, legal unit count, title and the survey are the usual rows.
- Update the row: Strategy, Verdict, Flags, Comps used, Rules that mattered (section 8). Append one line to Run log: date, stages run, what changed.
- Anything that did not fit a budget goes under "Research notes", which is a toggle block (`"type": "toggle"`, title "Research notes", content as its children so it opens collapsed), never a heading. The map code goes inside it as a code block, never as a file path.
- Last sale price and Last sale date on the row come from the latest deed in ACRIS even when the amount is $0 (write 0); Prior sale is the deed before it. Fill them on every row, deals and comps alike.
- Never edit the "Noah's notes" heading or anything below it.

## 7. Noah's defaults

Use these unless Noah gives a different number for a specific deal. Noah can edit this table. Cost, return and financing assumptions are deliberately absent until Noah has a basis for them.

| Assumption | Default |
| --- | --- |
| Comps scope | Closed within 18 months, half a mile, same product family; widen only when needed and say so |
| Exit comps | Only with a strategy; Flip renovated sales, Rent renovated comps with rents, Build land and new construction |
| Rents | Asking rents from StreetEasy history via rents-for-address; actual rents are an open item |

## 8. Notion map

- Real Estate → Underwriting Playbook (for Instinct): this page.
- Real Estate → Underwriting Template v5: the deal page and comp page shapes and budgets.
- Real Estate → Properties: Noah's older deal pages. New work is rows in the Properties database.
- Real Estate → Archive: older templates and side pages kept for reference. Never read or copy from it.
- Real Estate → NYC Zoning & Building Code: the ZR Sections and Definitions databases and "README for agents" with the query recipes.
- Real Estate → Properties database: https://www.notion.so/3fa9d8ce4a74811595f5c286b2ef5beb (id `3fa9d8ce-4a74-8115-95f5-c286b2ef5beb`). One row per building, keyed by the BBL property; the same table holds deals and comps. Find a row: `POST /v1/databases/3fa9d8ce-4a74-8115-95f5-c286b2ef5beb/query` with `{"filter": {"property": "BBL", "rich_text": {"equals": "3019840005"}}}`. Properties: Name (title, address), BBL, Role (Deal / Comp), Strategy (Flip / Rent / Build / Not set), Borough (select), Neighborhood (select), Zoning (multi-select), Lot (text "12.75 × 53" from PLUTO lotfront and lotdepth), Lot sf, Existing sf, Max ZFA, Flags (multi-select: Historic district, Landmark, Shallow lot, Near corner, Narrow lot, Irregular lot, Rent regulated?, Open DOB violations, Open HPD violations, Active DOB job, Flood zone, City owned, Litigation, No rent history), Units, Building (text in words from PLUTO bldgfront, bldgdepth, numfloors, yearbuilt and bldgclass: "20 × 58 ft · 2 floors · built 1910 · three-family walk-up"; a vacant lot says "Vacant land, zoned residential"), Verdict (Investigate / Pass / Closed by others), Noah's call (Pursue / Pass / Watch; Noah only, never set by you), Ask (number), Owner, Last sale price, Last sale date, Prior sale (text: "$600,000 · December 2025"), Sale $/sf (formula; never written), Beds/baths, Listing URL (the current listing for a deal, the sold listing for a comp), Comps used (relation to rows in this same database), Used by (its reverse; never written), Rules that mattered (relation to the ZR Sections database: the three or four section rows cited on the page; find a row with the filter Section ID equals "23-344" and use its page id). Nothing else: lot type, unused ratio, deal type, list price, days on market, the ZoLa link and the run date live on the page, not on the row (removed 2026-10-17).
- Example payload for a new deal row (`POST /v1/pages` with `"parent": {"database_id": "3fa9d8ce-4a74-8115-95f5-c286b2ef5beb"}`):

```json
{"Name": {"title": [{"text": {"content": "63 Irving Place"}}]},
 "BBL": {"rich_text": [{"text": {"content": "3019840005"}}]},
 "Role": {"select": {"name": "Deal"}}, "Strategy": {"select": {"name": "Build"}},
 "Borough": {"select": {"name": "Brooklyn"}}, "Zoning": {"multi_select": [{"name": "R6B"}]},
 "Lot": {"rich_text": [{"text": {"content": "12.75 × 53"}}]}, "Lot sf": {"number": 676},
 "Building": {"rich_text": [{"text": {"content": "Vacant land, zoned residential"}}]},
 "Max ZFA": {"number": 1352}, "Owner": {"rich_text": [{"text": {"content": "Minta Gillespie Walker Living Trust"}}]},
 "Flags": {"multi_select": [{"name": "Shallow lot"}, {"name": "Near corner"}, {"name": "Narrow lot"}]},
 "Verdict": {"select": {"name": "Investigate"}},
 "Comps used": {"relation": [{"id": "<page id of a comp row>"}]},
 "Rules that mattered": {"relation": [{"id": "<page id of the 23-22 row>"}, {"id": "<page id of the 23-344 row>"}]},
 "Ask": {"number": 499999}, "Listing URL": {"url": "https://www.zillow.com/homedetails/63-Irving-Pl-Brooklyn-NY-11238/112504346_zpid/"}}
```

- Example payload for a comp row: the same shape with `"Role": {"select": {"name": "Comp"}}`, `"Strategy": {"select": {"name": "Not set"}}`, `"Last sale price": {"number": 625000}`, `"Last sale date": {"date": {"start": "2025-09-30"}}`, `"Prior sale": {"rich_text": [{"text": {"content": "$600,000 · December 2025"}}]}` when there is one, Beds/baths and Listing URL from the listing pass, and no Ask, Verdict or Comps used.
- Saved routine: rents-for-address (your personal skill). Inside an underwriting job its table goes on the property's page under "Rents"; on its own, when Noah texts "rents for <address>", it answers in chat and writes nothing to Notion.
- Keys: the Google Maps Platform key (restricted to the Street View Static API and Places API (New), quota-capped) is in your vault as the login entry "Google Places API key" on places.googleapis.com; the same key serves Street View. Read it from the vault during the job. Never write it on a page, in a code block, in the Run log, in Research notes or in a message.
- Noah's laptop also has `scripts/screen.py` in ~/notion-underwriting, which runs Stages 0 to 3 from Open Data, draws both maps and writes the deal row and comp rows exactly as above. When a page already exists from the script, keep its structure, fill what it leaves out (photo, listing pass and Listing column, rents, exit comps) and update sentences 1 and 3 of the top paragraph instead of rebuilding it. The map code lives in that script; its layers and style are the reference for your own maps.

## 9. Budgets

| Section of the page | Budget |
| --- | --- |
| Top paragraph | 3 sentences, no labels |
| Details table | 9 rows; Finding cell 12 words; Field, Finding, Source only |
| Zoning | 1 buildable line + up to 3 rule entries of 3 lines each |
| Area | map + 1 caption line + grouped pin list (about 10) + 1 sentence only for a negative |
| Rents | 1 table, one row per unit, up to 8 rows; absent when there is no history |
| Purchase comps | map + up to 8 rows with the Listing column + 1 sentence |
| Exit comps | up to 8 rows + 1 sentence, only with a strategy |
| Open items | 6 rows |
| Run log | 1 line per run |
| Noah's notes | his; never edited |
| Comp page | photo, links, 1 to 2 sentences, details table of 5 rows, Rents table if any; 150 words excluding tables |
| Whole deal page excluding tables, the pin list, Research notes and Noah's notes | 450 words |
