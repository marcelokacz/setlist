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

Transition or stage notes can also be catalog rows. Give them `"type": "note"` and omit `length`, `bpm`, and `key`; they appear as lighter note tiles in the editor and as smaller parenthetical lines in the PDF. Notes do not affect song numbering, song counts, or running time. Notes are reusable: the pool keeps one copy available outside the setlist, while the setlist can contain at most one active copy.

Use **Download PDF** on the home page to enter the show date and location, then download the current in-setlist order with song details and notes.

PDF exports use the repository logo in [`FlowerLeaf Band Logo Black.png`](FlowerLeaf%20Band%20Logo%20Black.png).

Serve the repository over HTTP to load `songs.json`, for example:

```bash
python3 -m http.server 4173
```
