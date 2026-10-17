# Underwriting Template v5

Two page shapes live here: the deal page, and the lighter comp page at the bottom. Square brackets are instructions; delete them as you fill. The method lives in "Underwriting Playbook (for Instinct)" and never appears here. Nothing on a page is for Noah to fill in: his only input is "Noah's call" on the row. Omit any section that has nothing to say. Never write notes addressed to Noah or to yourself on the page.

---

## Deal page

[IMAGE: the front of the property. The listing's lead photo, uploaded to Notion; failing that, Google Street View; failing both, the links line begins "No photo · "]

[Listing](https://www.zillow.com/homedetails/63-Irving-Pl-Brooklyn-NY-11238/112504346_zpid/) · [StreetEasy](https://streeteasy.com/building/63-irving-place-brooklyn) · [ZoLa](https://zola.planning.nyc.gov/l/lot/3/1984/5) · [BIS](https://a810-bisweb.nyc.gov/bisweb/PropertyProfileOverviewServlet?bin=3393676) · [ACRIS](https://a836-acris.nyc.gov/bblsearch/bblsearch.asp?borough=3&block=1984&lot=5) · [DOF](https://propertyinformationportal.nyc.gov/parcels/parcel/3019840005)

[Each word above is itself the link (the example links point at 63 Irving Place); no bare URL anywhere on the page. With no live listing the first word is "Off market", linked to the property's Zillow or StreetEasy page.]

[Three sentences of plain prose, no labels. Sentence 1: "Investigate:" or "Pass:" then what it is and, when the strategy is set, what the strategy would make of it. Sentence 2: the ask against the best analog, per buildable sf for land or per sf for a building. Sentence 3: the one fact that decides it. Example: "Investigate: vacant 12.75 × 53 ft R6B interior lot in Clinton Hill that builds a 1,352 sf one- or two-family house. The ask is $370 per buildable sf; the one R6B lot of similar size sold at $223. A survey showing the lot sits within 100 ft of the Putnam corner removes the rear yard; failing that, the 1961 lot depth gives a 10 ft yard."]

### Floor plan

[Only if the listing has one. Image, no text.]

### Details

| Field | Finding | Source |
| --- | --- | --- |
| Ask | $499,999 · listed 2026-09-02 · 43 days on market | [listing] |
| Lot | 3-01984-0005 · BIN 3393676 · 12.75 × 53 ft, 676 sf, interior | [ZoLa] |
| Zoning | R6B · no overlay · no special district · not historic | [ZoLa] |
| Existing building | Vacant land · or: three-family walk-up · 3 units · built 1910 · 2 floors · 2,320 sf gross | [ZoLa] |
| Buildable | 676 × 2.0 = 1,352 sf · 0 built · 1,352 unused | [ZR 23-22 row] |
| Owner · last deed | Minta Gillespie Walker Living Trust · deed 2012-11-12 · $0, non-market | [ACRIS] |
| Violations · jobs | none open (DOB, ECB, HPD) · jobs: minor alteration, permit issued 2005 | [BIS], [HPD] |
| Taxes · rent regulation | $ per year · regulation signal · [only when the lot has units] | [DOF] |
| Flood | zone · [only when a zone is mapped] | [Flood Hazard Mapper] |

[9 rows max, Finding cell 12 words max, these Field names. Building classes and DOB codes in words, never codes. Every Source is a linked label to the lot-specific page; the lot record is called ZoLa on the page. An estimate says so in the cell ("about 63 ft, survey to confirm"). Delete rows that do not apply.]

### Zoning

[Only numbers specific to this lot, and only the rules that apply to it. Rules that apply to every lot in the district (height, coverage, standard yards, density) do not go here. Each rule is one entry of up to three lines: a plain sentence, the number for this lot, what proves it, and the link to the Notion row in the ZR Sections database. 3 rules max; the quoted text goes in Research notes.]

Buildable: 676 sf × FAR 2.0 = 1,352 sf ([ZR 23-22 row])

Rear yard, corner exemption: no rear yard is required within 100 ft of a street corner; the whole lot sits about 63 to 93 ft from the Putnam corner, estimated from lot centroids. A survey proves it. ([ZR 23-344 row])

Rear yard, shallow lot: a lot under 95 ft deep loses 6 in of rear yard per foot short, floor 10 ft; 30 − 0.5 × (95 − 53) = 10 ft. Proof of the lot's depth on December 15, 1961 is required. ([ZR 23-342 row])

Lot size: 12.75 ft wide and 676 sf, under the 18 ft and 1,700 sf minimums, but exempt as a zoning lot that existed on December 5, 2024 and has not shrunk since. ([ZR 23-10 row])

### Area

[Map per the playbook spec: street tiles cropped to the frame, which is a mile on a side (half a mile each way from the subject), dashed frame line, neighborhood outlines, red star for the subject, numbered pins in three color groups, no text in the image. Then, in this order: one caption line, the pin list as numbered-list blocks grouped by type with each line colored to match its pins, and one sentence only for something negative: historic district or flood zone. No new-building projects on the map or in the list, and no sentence on development pace.]

Map: OpenStreetMap tiles © OpenStreetMap contributors · NYC 2020 neighborhood boundaries · MTA stations · Google Places · NYC Parks · checked 2026-10-16 · straight-line miles

1. Halsey St (L) · subway · 0.20 mi [blue text, as are all train lines]
2. Wilson Av (L) · subway · 0.31 mi
3. Saraghina · restaurant · 4.6 (1,200 ratings) · 0.15 mi [red text, as are all food lines]
4. Irving Square Park · park, 2.4 acres · 0.22 mi [green text]

### Rents

[Only when the building has units and StreetEasy has history for it. One row per unit, asking rents from past listings, never called a rent roll. When there is no history the section is absent and the row's Flags says "No rent history".]

| Unit | Beds/baths | Last asking rent | Listed | StreetEasy |
| --- | --- | --- | --- | --- |
| 1 | 2 / 1 | $2,950 | March 2025 | [unit page] |
| 2 | 2 / 1 | $3,100 | August 2026 | [building page, when the unit has no page] |

### Purchase comps

[Map: same basemap and frame as the area map, numbered comps in table order, filled pin for a closed sale, hollow pin for a listing, no text in the image. Then every qualifying comp, up to 8 rows, nearest first: closed ACRIS deeds only, as-is sales of the same product family, each with its zoning district and what the listing pass found. Then one sentence naming the best analogs (same district, one-third to three times the subject's size) against the ask, and naming any lot that sold twice. No implied-value range.]

| # | Address | Closed | Price | Zoning | Area · basis | $/sf | Listing |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [address, linked to its ACRIS page] · 0.21 mi | date | $ | R6B | sf · buildable / building / marketed | $ | $1.25M list · 41 days · [link], or "not listed" |

Best analogs: #7 148 Madison Street at $223 per buildable sf; the ask is $370. The other rows are different districts or two to seven times the size.

### Exit comps

[Only when Strategy is set. Same table shape, up to 8 rows, one sentence. Flip: closed sales whose listing said renovated, gut renovated or new. Rent: renovated comps, and the sentence cites their rents per unit from their Rents tables. Build: land sales per buildable sf and new-construction sales.]

### Open items

| Missing fact | Moves the deal how | Evidence needed | Who |
| --- | --- | --- | --- |
| [fact] | [effect] | [document or record] | [Noah / architect / attorney] |

[6 rows max. Actual rents, legal unit count, title and the survey are the usual rows.]

Run log: [2026-10-16 · stages 0-3 · created]

▸ Research notes [a toggle block, collapsed, never a heading; no budget: rule quotes, precedents, BSA cases, long source notes, the map code as a code block]

### Noah's notes

[Noah's. The script and Instinct never edit this heading or anything below it.]

---

## Comp page

[For a row with Role Comp. 150 words excluding tables. No maps, no zoning block, no comps of its own.]

[IMAGE: the lead photo from the sold listing; failing that, Google Street View; failing both, the links line begins "No photo · "]

[Sold listing](https://www.zillow.com/homes/700-Monroe-St-Brooklyn-NY-11221_rb/) · [StreetEasy](https://streeteasy.com/building/700-monroe-street-brooklyn) · [ZoLa](https://zola.planning.nyc.gov/l/lot/3/1642/20) · [ACRIS](https://a836-acris.nyc.gov/bblsearch/bblsearch.asp?borough=3&block=1642&lot=20)

[One or two sentences: what it is, what it sold for and when, per sf on its basis, what the listing said about its condition, beds and baths, days on market. Example: "Converted two-family, 19.92 × 40 ft on a 20 × 100 R6B lot in Bedford-Stuyvesant; sold for $1,990,000 in July 2026, $1,248 per sf of building, after a gut renovation, having sold as-is for $600,000 in December 2025. Listed at $1,995,000, 4 beds 3 baths, 38 days on market."]

### Details

| Field | Finding | Source |
| --- | --- | --- |
| Lot | 3-01642-0020 · 20 × 100 ft, 2,000 sf, interior | [ZoLa] |
| Existing building | converted two-family · 2 units · built 1899 · 2 floors · 1,594 sf gross | [ZoLa] |
| Zoning | R6B · 3,984 sf allowed | [ZoLa] |
| Sales | $1,990,000 · 2026-07-30 · prior $600,000 · 2025-12-03 | [ACRIS] |
| Listing | $1,995,000 list · 4 / 3 · 38 days · renovated | [listing] |

### Rents

[Only when StreetEasy has history. Same table as the deal page.]

### Noah's notes

[Noah's. Never edited.]
