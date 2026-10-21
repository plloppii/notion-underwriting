# Instinct

Notes for Noah's assistant Instinct, on top of `AGENTS.md`. Everything else in this repository is agent-neutral.

- **No persistent workspace.** Your sandbox is wiped after a while, so every job starts with the two lines in `AGENTS.md`: clone if missing, then `sh ~/notion-underwriting/scripts/bootstrap.sh`. It pulls both repositories, installs the packages into your Python 3.10 and prints a check line. Your GitHub access covers the private repositories. If the map packages will not install, the bootstrap falls back to `requests` alone and the screen still runs; the page then has the pin list without the map images and the Run log says so.
- **Trigger.** Noah texts an address and borough, usually with a strategy word (Flip, Rent, Build), the asking price and a listing link. "rents for <address>" on its own runs your saved routine rents-for-address and answers in chat; nothing is written to Notion for that.
- **Keys.** The Notion integration token goes in `NOTION_TOKEN` before running the script. The Google Maps Platform key is the vault login entry "Google Places API key" on places.googleapis.com; export it as `GOOGLE_MAPS_API_KEY` for the script, or call Street View and Places with it directly as `docs/SOURCES.md` describes. Never write either key on a page, in a code block, in Run log, in Research notes or in a message.
- **Rents.** Your saved routine rents-for-address produces the Rents table from StreetEasy history (`docs/PLAYBOOK.md`, section 5). Inside a job its table goes on the page; on its own it answers in chat.
- **Browser steps** are exactly the ones in `docs/SOURCES.md` under "Browser only": the listing Noah sent, the listing pass on comps, StreetEasy, the DOF portal, HPD Online. Nothing else is opened in a browser: no map viewer, no zoning website, no ACRIS document images.
- **On the page**, the open items the script leaves to the assistant say "Instinct" in the Who column. `UW_AGENT` in the environment changes that name for another agent.
