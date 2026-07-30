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
import re
import ssl
import urllib.request
from datetime import datetime, timezone
from xml.etree import ElementTree as ET

_PLAYLIST_ID = "UUy9DdDXjlk_YLKG_r3ViXOg"
_CHANNEL_ID = "UCy9DdDXjlk_YLKG_r3ViXOg"
# Fallback para tratar clipes curtos como Shorts quando a URL /shorts falhar.
_SHORTS_FALLBACK_MAX_SECONDS = 180
USER_AGENT = "Mozilla/5.0 (compatible; ApostilaDevFastSync/1.0; +https://github.com/DanielLCintra/apostila-webdev)"
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_PATH = os.path.join(_ROOT, "assets", "data", "devfast-channel-videos.json")
_RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={_CHANNEL_ID}"
_MANUAL_VIDEOS = [
    {
        "videoId": "aIQmiS5pk80",
        "title": "Como é gravar um curso para a Alura? (Tudo o que não te contam)",
    },
]


def fetch_text(url: str, ctx: ssl.SSLContext) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45, context=ctx) as resp:
        return resp.read().decode("utf-8", errors="replace")


def is_short_by_duration(duration_sec: int | None) -> bool:
    return (
        duration_sec is not None
        and duration_sec <= _SHORTS_FALLBACK_MAX_SECONDS
    )


def is_youtube_short(video_id: str, duration_sec: int | None, ctx: ssl.SSLContext) -> bool:
    req = urllib.request.Request(
        f"https://www.youtube.com/shorts/{video_id}",
        headers={"User-Agent": USER_AGENT},
        method="HEAD",
    )
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
            return "/shorts/" in resp.geturl()
    except OSError:
        return is_short_by_duration(duration_sec)


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
                    if is_short_by_duration(length_sec):
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


def fetch_video_duration(video_id: str, ctx: ssl.SSLContext) -> int | None:
    html = fetch_text(f"https://www.youtube.com/watch?v={video_id}", ctx)
    m = re.search(r'"lengthSeconds":"(\d+)"', html)
    if m:
        return int(m.group(1))
    m = re.search(r'"approxDurationMs":"(\d+)"', html)
    if m:
        return round(int(m.group(1)) / 1000)
    return None


def read_existing_videos() -> list[dict]:
    if not os.path.exists(OUT_PATH):
        return []
    with open(OUT_PATH, encoding="utf-8") as f:
        payload = json.load(f)
    return payload.get("videos", [])


def fetch_rss_videos(ctx: ssl.SSLContext) -> list[dict]:
    root = ET.fromstring(fetch_text(_RSS_URL, ctx))
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
        "media": "http://search.yahoo.com/mrss/",
    }
    videos: list[dict] = []

    for entry in root.findall("atom:entry", ns):
        video_id_el = entry.find("yt:videoId", ns)
        title_el = entry.find("atom:title", ns)
        if video_id_el is None or title_el is None:
            continue

        video_id = video_id_el.text
        title = title_el.text
        if not video_id or not title:
            continue

        duration_sec = fetch_video_duration(video_id, ctx)
        if is_youtube_short(video_id, duration_sec, ctx):
            continue

        thumbnail = f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg"
        thumbnail_el = entry.find("media:group/media:thumbnail", ns)
        if thumbnail_el is not None:
            thumbnail = thumbnail_el.attrib.get("url", thumbnail)

        videos.append(
            {
                "videoId": video_id,
                "title": title,
                "durationSeconds": duration_sec,
                "thumbnail": thumbnail,
            }
        )

    return videos


def fetch_manual_videos(ctx: ssl.SSLContext) -> list[dict]:
    videos: list[dict] = []
    for video in _MANUAL_VIDEOS:
        video_id = video["videoId"]
        duration_sec = fetch_video_duration(video_id, ctx)
        if is_youtube_short(video_id, duration_sec, ctx):
            continue

        videos.append(
            {
                "videoId": video_id,
                "title": video["title"],
                "durationSeconds": duration_sec,
                "thumbnail": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
            }
        )

    return videos


def main() -> None:
    url = f"https://www.youtube.com/playlist?list={_PLAYLIST_ID}"
    ctx = ssl.create_default_context()
    html = fetch_text(url, ctx)

    data = extract_yt_initial_data(html)
    videos = dedupe_preserve_order(walk_playlist_videos(data)) if data else []
    if not videos:
        # O HTML da playlist muda com frequência. O RSS oficial traz os uploads
        # recentes; combinamos com o JSON existente para não perder o histórico.
        videos = dedupe_preserve_order(fetch_rss_videos(ctx) + read_existing_videos())
        if not videos:
            raise SystemExit(
                "Nenhum vídeo longo encontrado (todos foram filtrados como Shorts "
                "ou o YouTube não retornou itens)."
            )
    videos = dedupe_preserve_order(fetch_manual_videos(ctx) + videos)
    videos = [
        video
        for video in videos
        if not is_youtube_short(
            video["videoId"],
            video.get("durationSeconds"),
            ctx,
        )
    ]

    payload = {
        "channelId": _CHANNEL_ID,
        "playlistId": _PLAYLIST_ID,
        "channelUrl": "https://www.youtube.com/@DevFastOficial",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "note": (
            "Uploads do canal sem Shorts detectados pela URL /shorts; "
            f"fallback para clipes ≤ {_SHORTS_FALLBACK_MAX_SECONDS}s. "
            "O YouTube costuma carregar até ~100 itens por página da playlist."
        ),
        "excludedShortsFallbackMaxDurationSec": _SHORTS_FALLBACK_MAX_SECONDS,
        "videoCount": len(videos),
        "videos": videos,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"OK — {len(videos)} vídeos escritos em {OUT_PATH}")


if __name__ == "__main__":
    main()
