#!/usr/bin/env python3
"""Local, zero-dependency server for the ML4T study app.
- Serves the static app (index.html, data.js) from this folder.
- Persists notes + quiz progress to ../notes/ml4t_state.json (and a readable ml4t_notes.md).
- Read-only to your study files: it ONLY writes inside projects/ml4t_prep/notes/.
Run:  python3 serve.py    then open the printed URL.
"""
import http.server, socketserver, json, os, datetime, threading, shutil, glob

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES_DIR = os.path.join(os.path.dirname(HERE), "notes")
STATE = os.path.join(NOTES_DIR, "ml4t_state.json")
NOTES_MD = os.path.join(NOTES_DIR, "ml4t_notes.md")
BACKUP_DIR = os.path.join(NOTES_DIR, "_backups")
PORT = int(os.environ.get("ML4T_PORT", "8765"))
KEEP_BACKUPS = 60
_lock = threading.Lock()

def _backup_existing():
    """Snapshot the current state file BEFORE overwriting, so no write can lose data. Keeps last KEEP_BACKUPS."""
    if not os.path.exists(STATE):
        return
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    try:
        shutil.copy2(STATE, os.path.join(BACKUP_DIR, f"ml4t_state.{ts}.json"))
    except Exception:
        pass
    bks = sorted(glob.glob(os.path.join(BACKUP_DIR, "ml4t_state.*.json")))
    for old in bks[:-KEEP_BACKUPS]:
        try: os.remove(old)
        except Exception: pass

def write_state(obj):
    os.makedirs(NOTES_DIR, exist_ok=True)
    _backup_existing()  # preserve prior version first (recoverable)
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    os.replace(tmp, STATE)  # atomic
    # human-readable notes mirror (additive; never touches study_notes/ or slices/)
    notes = obj.get("notes", {})
    lines = ["# ML4T — My Notes",
             f"_Auto-written by the study app on {datetime.date.today().isoformat()}. {len(notes)} notes._\n"]
    for qid, txt in sorted(notes.items()):
        lines.append(f"## {qid}\n\n{txt}\n")
    with open(NOTES_MD, "w") as f:
        f.write("\n".join(lines))

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=HERE, **k)
    def log_message(self, *a):  # quiet
        pass
    def do_GET(self):
        if self.path.split("?")[0] == "/api/state":
            data = {}
            if os.path.exists(STATE):
                try: data = json.load(open(STATE))
                except Exception: data = {}
            body = json.dumps(data).encode()
            self.send_response(200); self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
            return
        return super().do_GET()
    def do_POST(self):
        if self.path.split("?")[0] == "/api/state":
            n = int(self.headers.get("Content-Length", "0"))
            try:
                obj = json.loads(self.rfile.read(n) or b"{}")
                with _lock: write_state(obj)
                self.send_response(204); self.end_headers()
            except Exception as e:
                self.send_response(400); self.end_headers(); self.wfile.write(str(e).encode())
            return
        self.send_response(404); self.end_headers()

if __name__ == "__main__":
    os.makedirs(NOTES_DIR, exist_ok=True)
    with socketserver.ThreadingTCPServer(("127.0.0.1", PORT), H) as httpd:
        print(f"ML4T study app → http://127.0.0.1:{PORT}/  (Ctrl-C to stop)")
        print(f"Notes/progress persist to: {STATE}")
        print(f"Readable notes mirror:     {NOTES_MD}")
        try: httpd.serve_forever()
        except KeyboardInterrupt: print("\nstopped")
