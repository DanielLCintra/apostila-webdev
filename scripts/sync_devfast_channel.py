#!/usr/bin/env python3
"""
Atualiza assets/data/devfast-channel-videos.json a partir da playlist de uploads
do canal DevFast no YouTube (todos os vídeos expostos na primeira página da
playlist — em geral até 100 itens).

Uso (na raiz do repositório):
  python3 scripts/sync_devfast_channel.py
"""

from __future__ import annotations

import json
import os
import ssl
import urllib.request
from datetime import datetime, timezone

_PLAYLIST_ID = "UUy9DdDXjlk_YLKG_r3ViXOg"
_CHANNEL_ID = "UCy9DdDXjlk_YLKG_r3ViXOg"
# Duração máxima (em segundos) para tratar como Short e não incluir na lista.
_SHORTS_MAX_SECONDS = 60
USER_AGENT = "Mozilla/5.0 (compatible; ApostilaDevFastSync/1.0; +https://github.com/DanielLCintra/apostila-webdev)"
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(_ROOT, "assets", "data", "devfast-channel-videos.json")


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
                if not vid or not title:
                    pass
                else:
                    length_sec: int | None
                    try:
                        raw_len = p.get("lengthSeconds")
                        length_sec = int(raw_len) if raw_len is not None else None
                    except (TypeError, ValueError):
                        length_sec = None
                    if length_sec is not None and length_sec <= _SHORTS_MAX_SECONDS:
                        pass
                    else:
                        found.append(
                            {
                                "videoId": vid,
                                "title": title,
                                "durationSeconds": length_sec,
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
        raise SystemExit(
            "Nenhum vídeo longo encontrado (todos foram filtrados como Shorts "
            f"≤ {_SHORTS_MAX_SECONDS}s ou a playlist não retornou itens)."
        )

    payload = {
        "channelId": _CHANNEL_ID,
        "playlistId": _PLAYLIST_ID,
        "channelUrl": "https://www.youtube.com/@DevFastOficial",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "note": (
            "Uploads do canal sem clipes ≤ "
            f"{_SHORTS_MAX_SECONDS}s (Shorts). "
            "O YouTube costuma carregar até ~100 itens por página da playlist."
        ),
        "excludedShortsMaxDurationSec": _SHORTS_MAX_SECONDS,
        "videoCount": len(videos),
        "videos": videos,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"OK — {len(videos)} vídeos escritos em {OUT_PATH}")


if __name__ == "__main__":
    main()
