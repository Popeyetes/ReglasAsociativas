#!/usr/bin/env python3
import json
import http.server
import socketserver
import threading
import webbrowser
import os
from algorithms import apriori, fp_growth, eclat

class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            try:
                with open('templates/index.html', 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.wfile.write(b"templates/index.html no encontrado")
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/analyze':
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body)
                transactions = data["transactions"]
                support = float(data["support"])
                confidence = float(data["confidence"])
                algo = data.get("algorithm", "apriori")

                if algo == "apriori":
                    rules, logs = apriori(transactions, support, confidence)
                elif algo == "fpgrowth":
                    rules, logs = fp_growth(transactions, support, confidence)
                elif algo == "eclat":
                    rules, logs = eclat(transactions, support, confidence)
                else:
                    rules, logs = apriori(transactions, support, confidence)

                result = json.dumps({"rules": rules, "logs": logs, "algorithm": algo})
            except Exception as e:
                result = json.dumps({"error": str(e)})

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(result.encode())
        else:
            self.send_response(404)
            self.end_headers()

def main():
    PORT = 8765
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"\n{'='*52}")
        print(f"  Minería de Reglas de Asociación (Modular)")
        print(f"  Algoritmos: A Priori · FP-Growth · ECLAT")
        print(f"{'='*52}")
        print(f"  Abre tu navegador en: {url}")
        print(f"  Presiona Ctrl+C para detener")
        print(f"{'='*52}\n")
        threading.Thread(target=lambda: webbrowser.open(url), daemon=True).start()
        httpd.serve_forever()

if __name__ == "__main__":
    main()
