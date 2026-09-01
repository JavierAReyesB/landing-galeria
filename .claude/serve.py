"""Servidor estatico local para el catalogo.

Emula lo que hace `npx serve`, que es lo que asume el sitio:
  - URLs limpias: /viewer -> viewer.html (el catalogo enlaza `viewer?t=<slug>`).
  - HTTP/1.1 con keep-alive.
  - Range requests (206), imprescindible para que el navegador reproduzca
    los .mp4 locales en streaming en vez de descargarlos enteros.
"""
import functools
import http.server
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNK = 64 * 1024
RANGE_RE = re.compile(r"bytes=(\d*)-(\d*)$")


class StaticHandler(http.server.SimpleHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def translate_path(self, path):
        local = super().translate_path(path)
        if not os.path.exists(local) and not os.path.splitext(local)[1]:
            html = local + ".html"
            if os.path.isfile(html):
                return html
        return local

    def end_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        # Servidor de desarrollo: revalidar siempre, para que al editar un
        # index.html el navegador no siga sirviendo la version cacheada.
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def do_GET(self):
        header = self.headers.get("Range")
        path = self.translate_path(self.path)
        if header and os.path.isfile(path):
            match = RANGE_RE.match(header.strip())
            if match:
                self.serve_range(path, *match.groups())
                return
        super().do_GET()

    def serve_range(self, path, first, last):
        size = os.path.getsize(path)
        if first == "":
            # Sufijo: los ultimos N bytes (el moov de un mp4 suele ir al final).
            start, end = max(0, size - int(last or 0)), size - 1
        else:
            start = int(first)
            end = min(int(last), size - 1) if last else size - 1

        if start >= size or start > end:
            self.send_response(416)
            self.send_header("Content-Range", "bytes */%d" % size)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        length = end - start + 1
        self.send_response(206)
        self.send_header("Content-Type", self.guess_type(path))
        self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
        self.send_header("Content-Length", str(length))
        self.end_headers()

        with open(path, "rb") as handle:
            handle.seek(start)
            while length > 0:
                chunk = handle.read(min(CHUNK, length))
                if not chunk:
                    break
                self.wfile.write(chunk)
                length -= len(chunk)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
    handler = functools.partial(StaticHandler, directory=ROOT)
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
