#!/usr/bin/env python3
"""
Fetch auto-subtitles from the AI Engineer YouTube channel and write
one markdown file per talk to transcripts/.

Usage:
    python scripts/fetch_transcripts.py [--after YYYYMMDD] [--limit N]

Defaults: --after 20250101, --limit 20
"""

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

CHANNEL_URL = "https://www.youtube.com/@aiDotEngineer/videos"
TRANSCRIPTS_DIR = Path("transcripts")
MANIFEST_FILE = TRANSCRIPTS_DIR / "_manifest.json"


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")[:60]


def load_manifest() -> dict:
    if MANIFEST_FILE.exists():
        return json.loads(MANIFEST_FILE.read_text())
    return {}


def save_manifest(manifest: dict) -> None:
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2))


def fetch_channel_videos(after: str, limit: int) -> list[dict]:
    """Return video metadata list from yt-dlp, filtered and sorted.

    Uses full (non-flat) metadata fetch so upload_date is populated.
    The /videos page is sorted newest-first; --break-on-reject stops
    once we fall below --dateafter, keeping runtime bounded.
    We fetch up to 4× limit as a lookahead window before filtering.
    """
    lookahead = max(limit * 4, 100)
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-warnings",
        "--skip-download",
        "--dateafter", after,
        "--break-on-reject",
        "--playlist-end", str(lookahead),
        CHANNEL_URL,
    ]
    print(f"Fetching channel metadata from {CHANNEL_URL} (lookahead={lookahead}) ...", flush=True)
    result = subprocess.run(cmd, capture_output=True, text=True)
    # yt-dlp exits non-zero when --break-on-reject fires; that's expected
    if result.returncode not in (0, 1) and not result.stdout.strip():
        print(f"yt-dlp error:\n{result.stderr}", file=sys.stderr)
        sys.exit(1)

    after_dt = datetime.strptime(after, "%Y%m%d")
    videos = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        try:
            v = json.loads(line)
        except json.JSONDecodeError:
            continue

        # Filter out shorts (duration < 120s), live streams, member-only
        duration = v.get("duration") or 0
        if duration < 120:
            continue
        if v.get("is_live"):
            continue
        if v.get("availability") in ("subscriber_only", "needs_auth", "premium_only"):
            continue

        upload_date = v.get("upload_date", "")
        if not upload_date or len(upload_date) != 8:
            continue
        try:
            upload_dt = datetime.strptime(upload_date, "%Y%m%d")
        except ValueError:
            continue
        if upload_dt < after_dt:
            continue

        videos.append(v)

    # Sort ascending by upload date, take first N
    videos.sort(key=lambda v: v.get("upload_date", ""))
    return videos[:limit]


def extract_speaker_from_title(title: str) -> str:
    """Best-effort: grab text after last '-' or '|' as speaker hint."""
    for sep in [" | ", " - ", ": "]:
        if sep in title:
            parts = title.split(sep)
            # Last segment often has speaker or event
            return parts[-1].strip()
    return ""


def fetch_transcript(video_id: str, video_url: str) -> str | None:
    """Download auto-subtitles and return plain text, or None if unavailable."""
    with tempfile.TemporaryDirectory() as tmpdir:
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--sub-format", "vtt",
            "--no-warnings",
            "--output", os.path.join(tmpdir, "%(id)s.%(ext)s"),
            video_url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        # Find the .vtt file
        vtt_files = list(Path(tmpdir).glob("*.vtt"))
        if not vtt_files:
            return None
        raw = vtt_files[0].read_text(encoding="utf-8", errors="replace")
        return vtt_to_text(raw)


def vtt_to_text(vtt: str) -> str:
    """Strip VTT timing lines and deduplicate rolling captions."""
    lines = vtt.splitlines()
    text_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("WEBVTT") or line.startswith("NOTE"):
            continue
        # Timing line: 00:00:00.000 --> 00:00:00.000
        if re.match(r"^\d{2}:\d{2}:\d{2}[\.,]\d{3}\s*-->\s*\d{2}:\d{2}:\d{2}[\.,]\d{3}", line):
            continue
        # Remove inline VTT tags like <00:00:00.000> or <c>
        line = re.sub(r"<[^>]+>", "", line)
        line = line.strip()
        if line:
            text_lines.append(line)

    # Deduplicate consecutive duplicate lines (rolling caption artifact)
    deduped = []
    prev = None
    for line in text_lines:
        if line != prev:
            deduped.append(line)
        prev = line
    return "\n".join(deduped)


def write_transcript(video: dict, transcript_text: str) -> Path:
    upload_date = video.get("upload_date", "00000000")
    date_fmt = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"
    title = video.get("title", video.get("id", "unknown"))
    speaker = extract_speaker_from_title(title)
    title_slug = slugify(title)
    speaker_slug = slugify(speaker) if speaker else "unknown"

    filename = f"{date_fmt}-{speaker_slug}-{title_slug}.md"
    filepath = TRANSCRIPTS_DIR / filename

    frontmatter = f"""---
speaker: {speaker or "unknown"}
event: AI Engineer
date: {date_fmt}
youtube_url: https://www.youtube.com/watch?v={video['id']}
---

"""
    filepath.write_text(frontmatter + transcript_text, encoding="utf-8")
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Fetch AI Engineer talk transcripts")
    parser.add_argument("--after", default="20250101", help="Fetch videos uploaded on or after YYYYMMDD")
    parser.add_argument("--limit", type=int, default=20, help="Max number of videos to fetch")
    args = parser.parse_args()

    TRANSCRIPTS_DIR.mkdir(exist_ok=True)
    manifest = load_manifest()

    videos = fetch_channel_videos(args.after, args.limit)
    print(f"Found {len(videos)} eligible videos (after filtering, before manifest check).")

    new_count = 0
    skipped_count = 0
    unprocessable_count = 0

    for video in videos:
        vid_id = video.get("id")
        if not vid_id:
            continue
        if vid_id in manifest:
            print(f"  skip (manifest): {video.get('title', vid_id)}")
            skipped_count += 1
            continue

        title = video.get("title", vid_id)
        print(f"  fetching: {title}")
        video_url = f"https://www.youtube.com/watch?v={vid_id}"
        transcript = fetch_transcript(vid_id, video_url)

        if not transcript or len(transcript.strip()) < 100:
            print(f"    -> unprocessable (no usable subtitles)")
            manifest[vid_id] = {"status": "unprocessable", "title": title}
            unprocessable_count += 1
        else:
            filepath = write_transcript(video, transcript)
            print(f"    -> {filepath}")
            manifest[vid_id] = {
                "status": "ok",
                "title": title,
                "file": str(filepath),
                "upload_date": video.get("upload_date"),
            }
            new_count += 1

        save_manifest(manifest)

    print(f"\nDone. {new_count} new, {skipped_count} skipped, {unprocessable_count} unprocessable.")


if __name__ == "__main__":
    main()
