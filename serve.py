"""Serve dist/ for local preview (threaded to handle concurrent requests)"""
import http.server, os, sys, socketserver

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist"))
port = int(sys.argv[1]) if len(sys.argv) > 1 else 8096


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # silence logs


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True


print(f"Serving dist/ on http://localhost:{port} (threaded)")
ThreadedHTTPServer(("", port), Handler).serve_forever()
