# Dev Notes

Setup gotchas and implementation notes.

## fetch_transcripts.py — yt-dlp channel metadata quirks

### `--flat-playlist` does not populate `upload_date`

- **Symptom**: Script found 0 eligible videos despite the channel having hundreds.
- **Cause**: `--flat-playlist` returns lightweight playlist entries where `upload_date` and `timestamp` are `null`. The Python-side date filter then dropped everything.
- **Fix**: Removed `--flat-playlist`. Full metadata fetch (`--dump-json` without flat mode) populates `upload_date` correctly.

### Channel URL must include `/videos`

- **Symptom**: Same 0-result issue on the bare `@aiDotEngineer` handle.
- **Fix**: Use `https://www.youtube.com/@aiDotEngineer/videos`. The `/videos` tab is sorted newest-first and is the correct playlist endpoint for scripted access.

### `--break-on-reject` exits with code 1 — that's expected

- The channel is sorted newest-first. Combined with `--dateafter`, yt-dlp rejects videos once it falls below the date threshold and exits with code 1.
- The script treats exit codes 0 and 1 as both acceptable (only fails if stdout is also empty).

## Python invocation

Use `python3`, not `python` — `python` is not in PATH on this WSL environment.
