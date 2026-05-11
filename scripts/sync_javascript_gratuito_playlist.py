#!/usr/bin/env python3
"""
Gera assets/data/javascript-gratuito-youtube-videos.json a partir da playlist
pública do curso gratuito de JavaScript (DevFast).

Uso (na raiz do repositório):
  python3 scripts/sync_javascript_gratuito_playlist.py
"""

from __future__ import annotations

import json
import os
import ssl
import urllib.request
from datetime import datetime, timezone

_PLAYLIST_ID = "PLVqMckwJhEhbZho9gdClTsK6xucXgXd0-"
_PLAYLIST_URL = (
    "https://www.youtube.com/watch?v=uitVg1TyrRQ"
    f"&list={_PLAYLIST_ID}"
)
USER_AGENT = "Mozilla/5.0 (compatible; ApostilaJSCursoSync/1.0)"
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(_ROOT, "assets", "data", "javascript-gratuito-youtube-videos.json")


def extract_yt_initial_data(html: str) -> dict | None:
    marker = "var ytInitialData = "
    idx = html.find(marker)
    if idx == -1:
        return None
    i = idx + len(marker)
    if i >= len(html) or html[i] != "{":
        return None
    depth = 0
    for j in range(i, len(html)):
        c = html[j]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return json.loads(html[i : j + 1])
    return None


def walk_playlist_videos(obj) -> list[dict]:
    found: list[dict] = []

    def inner(o):
        if isinstance(o, dict):
            if "playlistVideoRenderer" in o:
                p = o["playlistVideoRenderer"]
                vid = p.get("videoId")
                title = None
                try:
                    title = p["title"]["runs"][0]["text"]
                except (KeyError, IndexError):
                    title = p.get("title", {}).get("simpleText")
                if vid and title:
                    found.append(
                        {
                            "videoId": vid,
                            "title": title,
                            "thumbnail": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
                        }
                    )
            for v in o.values():
                inner(v)
        elif isinstance(o, list):
            for item in o:
                inner(item)

    inner(obj)
    return found


def dedupe_preserve_order(items: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out: list[dict] = []
    for it in items:
        vid = it["videoId"]
        if vid not in seen:
            seen.add(vid)
            out.append(it)
    return out


def main() -> None:
    url = f"https://www.youtube.com/playlist?list={_PLAYLIST_ID}"
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45, context=ctx) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    data = extract_yt_initial_data(html)
    if not data:
        raise SystemExit("Não foi possível localizar ytInitialData na página da playlist.")

    videos = dedupe_preserve_order(walk_playlist_videos(data))
    if not videos:
        raise SystemExit("Nenhum vídeo encontrado nesta playlist.")

    payload = {
        "playlistId": _PLAYLIST_ID,
        "playlistUrl": _PLAYLIST_URL,
        "title": "Curso gratuito de JavaScript (DevFast)",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "note": "Ordem da playlist = ordem sugerida das aulas.",
        "videoCount": len(videos),
        "videos": videos,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"OK — {len(videos)} aulas escritas em {OUT_PATH}")


if __name__ == "__main__":
    main()
