from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

DEMO_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = DEMO_ROOT.parent.parent


class DemoHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Strip query string / fragment before resolving.
        path = path.split('?', 1)[0].split('#', 1)[0]
        rel = path.lstrip('/')
        # Canonical figures live under reports/visual_evidence/; the demo page
        # references them as ../visual_evidence/... (browser normalizes ".." away).
        if rel.startswith('visual_evidence/'):
            return str(DEMO_ROOT.parent / rel)
        # experiments/ lives at the project root.
        if rel.startswith('experiments/'):
            return str(PROJECT_ROOT / rel)
        # Everything else is demo-local (index.html, demo_payload.json).
        return str(DEMO_ROOT / rel)

    def log_message(self, fmt, *args):
        print('%s - %s' % (self.address_string(), fmt % args), flush=True)


port = int(sys.argv[1]) if len(sys.argv) > 1 else 4173
ThreadingHTTPServer(('127.0.0.1', port), DemoHandler).serve_forever()
