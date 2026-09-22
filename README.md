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

Serve the repository over HTTP to load `songs.json`, for example:

```bash
python3 -m http.server 4173
```
