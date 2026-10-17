#!/usr/bin/env python
"""Publish docs/UNDERWRITING_PLAYBOOK.md and docs/DEAL_TEMPLATE.md as Notion pages under the Real Estate page.

Env: NOTION_TOKEN or NOTION_API_TOKEN; NOTION_UW_PARENT overrides the parent page id.
Re-running updates both pages in place (URLs stay stable). Page ids live in data/notion_state.json under "pages".
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from notion_api import append, list_children, load_state, md_to_blocks, page_url, req, rt, save_state  # noqa: E402

PARENT = os.environ.get("NOTION_UW_PARENT", "60a139f3-f569-40cf-9976-8d0c40dae1c5")  # "Real Estate"
PAGES = {
    "underwriting_playbook": ("Underwriting Playbook (for Instinct)", "📐", ROOT / "docs" / "UNDERWRITING_PLAYBOOK.md"),
    "deal_template": ("Underwriting Template v5", "📄", ROOT / "docs" / "DEAL_TEMPLATE.md"),
}


def publish(state: dict, key: str, title: str, emoji: str, path: Path) -> str:
    md = path.read_text()
    # drop the H1: the page title carries it
    lines = md.splitlines()
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    blocks = md_to_blocks("\n".join(lines))
    print(f"{key}: {len(blocks)} blocks from {path.relative_to(ROOT)}")
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
    only = sys.argv[1:] or list(PAGES)
    state = load_state()
    for key in only:
        title, emoji, path = PAGES[key]
        pid = publish(state, key, title, emoji, path)
        print(f"  {title}: {page_url(pid)}")


if __name__ == "__main__":
    main()
