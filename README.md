# Setlist

A small browser-based setlist planner.

## Song catalog

Song metadata lives in [`songs.json`](songs.json), so it can be versioned and edited directly in the repository. Each song has this shape:

```json
{
	"id": "sandman",
	"title": "Sandman",
	"length": "05:08",
	"bpm": 92,
	"key": "D",
	"inSetlist": true
}
```

The page fetches the catalog when it loads. Dragging and reordering songs is saved separately in browser local storage, keeping the repository catalog as the source of truth for song details. The current design supports up to 100 rows without needing a database server.

## Saved setlists

Named setlists are stored as JSON files in the repository's `setlists/` directory. Run the included server to enable the **Save to repository** and **Load** controls:

Serve the repository over HTTP to load `songs.json`, for example:

```bash
python3 server.py
```

The server runs at `http://localhost:4173`. Saving a setlist creates or replaces `setlists/<name>.json`, which can be committed with the rest of the repository. If the page is served by a static server instead, saving downloads a JSON snapshot as a fallback.
