from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

DEMO_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = DEMO_ROOT.parent.parent


class DemoHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Strip query string / fragment before resolving.
        path = path.split('?', 1)[0].split('#', 1)[0]
        # Demo-local files (index.html, demo_payload.json) take priority.
        demo_path = DEMO_ROOT / path.lstrip('/')
        if demo_path.exists():
            return str(demo_path)
        # Fall back to the project root so canonical assets in
        # visual_evidence/, experiments/, reports/, outputs/ resolve.
        return str(PROJECT_ROOT / path.lstrip('/'))

    def log_message(self, fmt, *args):
        print('%s - %s' % (self.address_string(), fmt % args), flush=True)


port = int(sys.argv[1]) if len(sys.argv) > 1 else 4173
ThreadingHTTPServer(('127.0.0.1', port), DemoHandler).serve_forever()
