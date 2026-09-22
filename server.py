from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse
import json
import re

ROOT = Path(__file__).resolve().parent
SETLISTS = ROOT / 'setlists'
SETLISTS.mkdir(exist_ok=True)


def slugify(name):
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    return slug[:80] or 'untitled-setlist'


class SetlistHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/setlists':
            self.send_json(self.list_setlists())
            return
        if path.startswith('/api/setlists/'):
            slug = unquote(path.rsplit('/', 1)[-1])
            file_path = SETLISTS / f'{slug}.json'
            if file_path.is_file():
                self.send_json(json.loads(file_path.read_text()))
            else:
                self.send_error(404, 'Setlist not found')
            return
        super().do_GET()

    def do_POST(self):
        if urlparse(self.path).path != '/api/setlists':
            self.send_error(404, 'Not found')
            return
        try:
            payload = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))))
            name = str(payload.get('name', '')).strip()
            if not name:
                raise ValueError('A setlist name is required')
            setlist = {
                'name': name,
                'savedAt': payload.get('savedAt'),
                'in': payload.get('in', []),
                'out': payload.get('out', [])
            }
            file_path = SETLISTS / f'{slugify(name)}.json'
            file_path.write_text(json.dumps(setlist, indent=2) + '\n')
            self.send_json({'slug': file_path.stem, **setlist}, status=201)
        except (ValueError, json.JSONDecodeError) as error:
            self.send_json({'error': str(error)}, status=400)

    def list_setlists(self):
        setlists = []
        for file_path in sorted(SETLISTS.glob('*.json'), key=lambda path: path.stat().st_mtime, reverse=True):
            try:
                data = json.loads(file_path.read_text())
                setlists.append({'slug': file_path.stem, 'name': data.get('name', file_path.stem), 'savedAt': data.get('savedAt')})
            except json.JSONDecodeError:
                continue
        return setlists

    def send_json(self, payload, status=200):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    print('Setlist running at http://localhost:4173')
    ThreadingHTTPServer(('0.0.0.0', 4173), SetlistHandler).serve_forever()
