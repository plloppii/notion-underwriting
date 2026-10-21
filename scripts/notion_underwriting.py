#!/usr/bin/env python
"""Keep the two Notion instruction pages, "Underwriting Playbook (for Instinct)" and "Underwriting Template v5", pointing at
this repository. Since 2026-10-21 docs/UNDERWRITING_PLAYBOOK.md and docs/DEAL_TEMPLATE.md are the only maintained copies and
Instinct reads them from its clone of the repository; the Notion pages exist so old links resolve.

Default: each page's body becomes one paragraph linking to the file on GitHub. `--mirror` publishes the full markdown instead
(the pre-2026-10-21 behaviour) for a one-off read in Notion. Positional keys limit the run to one page.

Env: NOTION_TOKEN or NOTION_API_TOKEN; NOTION_UW_PARENT overrides the parent page id. Re-running updates both pages in place
(URLs stay stable). Page ids live in data/notion_state.json under "pages".
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from notion_api import append, list_children, load_state, md_to_blocks, page_url, req, rt, save_state  # noqa: E402

PARENT = os.environ.get("NOTION_UW_PARENT", "60a139f3-f569-40cf-9976-8d0c40dae1c5")  # "Real Estate"
REPO = "https://github.com/plloppii/notion-underwriting"
PAGES = {
    "underwriting_playbook": ("Underwriting Playbook (for Instinct)", "📐", ROOT / "docs" / "UNDERWRITING_PLAYBOOK.md"),
    "deal_template": ("Underwriting Template v5", "📄", ROOT / "docs" / "DEAL_TEMPLATE.md"),
}


def pointer_md(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    return (f"Moved to GitHub on 2026-10-21. The maintained copy is [{rel}]({REPO}/blob/main/{rel}) in the notion-underwriting "
            f"repository: clone or pull it and read the file there. Nothing on this page is current, and editing it changes nothing.")


def body_blocks(path: Path, mirror: bool) -> list[dict]:
    if not mirror:
        return md_to_blocks(pointer_md(path))
    lines = path.read_text().splitlines()
    if lines and lines[0].startswith("# "):  # the page title carries the H1
        lines = lines[1:]
    return md_to_blocks("\n".join(lines))


def publish(state: dict, key: str, title: str, emoji: str, path: Path, mirror: bool) -> str:
    blocks = body_blocks(path, mirror)
    print(f"{key}: {len(blocks)} blocks ({'full mirror' if mirror else 'pointer'}) for {path.relative_to(ROOT)}")
    pages = state.setdefault("pages", {})
    page_id = pages.get(key)
    if page_id:
        try:
            p = req("GET", f"/pages/{page_id}")
            if p.get("archived") or p.get("in_trash"):
                page_id = None
        except RuntimeError:
            page_id = None
    if page_id:
        old = list_children(page_id)
        print(f"  updating in place: removing {len(old)} old blocks")
        for b in old:
            req("DELETE", f"/blocks/{b['id']}")
        req("PATCH", f"/pages/{page_id}", {"properties": {"title": {"title": rt(title)}},
                                           "icon": {"type": "emoji", "emoji": emoji}})
        append(page_id, blocks)
    else:
        p = req("POST", "/pages", {"parent": {"page_id": PARENT}, "icon": {"type": "emoji", "emoji": emoji},
                                   "properties": {"title": {"title": rt(title)}}, "children": blocks[:100]})
        page_id = p["id"]
        append(page_id, blocks[100:])
        pages[key] = page_id
        save_state(state)
    return page_id


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("keys", nargs="*", metavar="KEY", help=f"limit to these pages (default: both): {', '.join(PAGES)}")
    ap.add_argument("--mirror", action="store_true", help="publish the full markdown instead of the pointer paragraph")
    args = ap.parse_args()
    if bad := [k for k in args.keys if k not in PAGES]:
        ap.error(f"unknown page key(s): {', '.join(bad)}")
    state = load_state()
    for key in args.keys or list(PAGES):
        title, emoji, path = PAGES[key]
        pid = publish(state, key, title, emoji, path, args.mirror)
        print(f"  {title}: {page_url(pid)}")


if __name__ == "__main__":
    main()
