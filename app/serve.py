#!/usr/bin/env python3
"""Local, zero-dependency server for the ML4T study app (Python 3.8+, standard library only).
- Serves the static app (index.html, data.js) from this folder.
- Persists notes + quiz progress to user-data/ml4t_state.json (and a readable ml4t_notes.md).
  It ONLY writes inside that folder.
- Serves book PDFs read-only from books/ at /books/<exact filename>.pdf (side-panel reader), if you add them.
Run:  python3 app/serve.py [--open] [--lan]    then open the printed URL.
--lan: also serve to devices on your local Wi-Fi (e.g. your phone). Off by default. LAN clients must
       open the printed link once (it carries a random access key, kept in user-data/lan_key.txt);
       requests from outside private address ranges are refused.
Env overrides: ML4T_PORT, ML4T_NOTES_DIR, ML4T_BACKUP_DIR, ML4T_BOOKS_DIR, ML4T_DATA_JS (serve a different data.js
build), ML4T_ROOT (allowed folder(s) for --lan, separated by ":").
"""
import http.server, socketserver, json, os, re, sys, secrets, hmac, ipaddress, socket, datetime, threading, shutil, glob, urllib.parse, webbrowser

HERE = os.path.dirname(os.path.abspath(__file__))
APPROOT = os.path.dirname(HERE)
NOTES_DIR = os.environ.get("ML4T_NOTES_DIR") or os.path.join(APPROOT, "user-data")
STATE = os.path.join(NOTES_DIR, "ml4t_state.json")
NOTES_MD = os.path.join(NOTES_DIR, "ml4t_notes.md")
BACKUP_DIR = os.environ.get("ML4T_BACKUP_DIR") or os.path.join(NOTES_DIR, "_backups")   # rolling snapshots (can live off cloud sync)
BOOKS_DIR = os.environ.get("ML4T_BOOKS_DIR") or os.path.join(APPROOT, "books")   # read-only: PDFs for the side-panel reader
DATA_JS = os.environ.get("ML4T_DATA_JS")   # optional alternate data.js (e.g. a build with personal extras)
PORT = int(os.environ.get("ML4T_PORT", "8765"))
KEEP_BACKUPS = 60
# Everything the server may read or write must live under this folder (realpath-checked). Default = the
# study-app folder; a personal launcher may widen it to the project folder that holds notes/ and books/.
ROOTS = [os.path.realpath(r) for r in (os.environ.get("ML4T_ROOT") or APPROOT).split(os.pathsep) if r]
ROOT = os.pathsep.join(ROOTS)   # for messages
def inside_root(p):
    return p is not None and any((os.path.realpath(p) + os.sep).startswith(r + os.sep) for r in ROOTS)
# REMOTE (any non-localhost client, even with the LAN key) is read-mostly by design:
#  - GET only the app page, its data, the saved state, the book list and book PDFs — nothing else;
#  - POST only /api/state: a validated, size-limited, ADDITIVE save (merged into the saved state —
#    it can add or update entries but never remove them), and it never prunes/deletes backup files;
#  - no other methods, no directory listings, no file paths, no command execution of any kind.
REMOTE_GET = {"/", "/index.html", "/data.js", "/api/state", "/api/books"}
STATE_KEYS = {"notes", "attempts", "seen", "reviewed", "reviewLog", "flagged", "box", "lastQuiz", "ui", "week", "week2", "_rev"}
MAX_POST = 5 * 1024 * 1024
LAN = "--lan" in sys.argv
LAN_KEY_FILE = os.path.join(NOTES_DIR, "lan_key.txt")
LAN_KEY = None   # set at startup when --lan
# optional extra layer: only these LAN IPs (comma-separated), e.g. ML4T_LAN_ALLOW=192.168.1.23 — the key is still required
def lan_networks():
    """Subnets of the computer's Wi-Fi/Ethernet interfaces (en*/eth*/wl*), NOT VPN tunnels (utun*, tun*,
    ppp*) — so only devices on your own home network qualify. Falls back to None (= any private IP)."""
    import subprocess
    try:
        out = subprocess.run(["ifconfig"], capture_output=True, text=True, timeout=3).stdout
    except Exception:
        return None
    nets, iface = [], ""
    for line in out.splitlines():
        if line and not line[0].isspace():
            iface = line.split(":")[0]
        m = re.search(r"inet (\d+\.\d+\.\d+\.\d+) netmask (0x[0-9a-f]+)", line)
        if m and re.match(r"(en|eth|wl)", iface):
            mask = ipaddress.IPv4Address(int(m.group(2), 16))
            nets.append((iface, ipaddress.IPv4Interface(f"{m.group(1)}/{mask}")))
    return nets or None
LAN_NETS = lan_networks() if LAN else None
LAN_ALLOW = {x.strip() for x in os.environ.get("ML4T_LAN_ALLOW", "").split(",") if x.strip()}
_lock = threading.Lock()

def _backup_existing(prune=True):
    """Snapshot the current state file BEFORE overwriting, so no write can lose data. Keeps last KEEP_BACKUPS."""
    if not os.path.exists(STATE):
        return
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")   # unique per save: a backup is never overwritten
    try:
        shutil.copy2(STATE, os.path.join(BACKUP_DIR, f"ml4t_state.{ts}.json"))
    except Exception:
        pass
    bks = sorted(glob.glob(os.path.join(BACKUP_DIR, "ml4t_state.*.json")))
    for old in (bks[:-KEEP_BACKUPS] if prune else []):   # remote saves never delete files
        try: os.remove(old)
        except Exception: pass

def read_state():
    if os.path.exists(STATE):
        try: return json.load(open(STATE))
        except Exception: return {}
    return {}

def merge_state(cur, inc):
    """A save from a device that hadn't seen the latest state (phone + Mac both open): keep both.
    Per-question maps are unioned (incoming wins on the same key); reviewLog keeps the larger daily count.
    Deletions made on the stale device (e.g. an un-flag) may be undone — re-apply them if so."""
    out = dict(cur)
    for k, v in inc.items():
        if k == "_rev": continue
        if k == "reviewLog" and isinstance(v, dict):
            rl = dict(cur.get(k) or {})
            for d, n in v.items(): rl[d] = max(n, rl.get(d, 0))
            out[k] = rl
        elif isinstance(v, dict) and isinstance(cur.get(k), dict) and k != "ui":
            out[k] = {**cur[k], **v}
        else:
            out[k] = v
    return out

def write_state(obj, prune=True):
    os.makedirs(NOTES_DIR, exist_ok=True)
    _backup_existing(prune)  # preserve prior version first (recoverable)
    tmp = STATE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    os.replace(tmp, STATE)  # atomic
    # human-readable notes mirror (additive; never touches study_notes/ or slices/)
    notes = obj.get("notes", {})
    lines = ["# ML4T — My Notes",
             f"_Auto-written by the study app on {datetime.date.today().isoformat()}. {len(notes)} notes. "
             "Grouped by exam → part → domain, in question order._\n"]
    def key(qid):  # "QF2-D6G5Q2" → (exam 2, "QF", 6, 5, 2)
        m = re.match(r"(ML|QF)(2?)-D(\d+)G(\d+)Q(\d+)", qid)
        return (2 if m.group(2) else 1, m.group(1), int(m.group(3)), int(m.group(4)), int(m.group(5))) if m else (9, qid, 0, 0, 0)
    last = (None, None, None)
    for qid in sorted(notes, key=key):
        ex, part, dom = key(qid)[:3]
        if ex != last[0]: lines.append(f"# Exam {ex}\n")
        if (ex, part) != last[:2]: lines.append(f"## {'Machine Learning (ML)' if part == 'ML' else 'Quantitative Finance (QF)'}\n")
        if (ex, part, dom) != last: lines.append(f"### {part}-D{dom}\n")
        last = (ex, part, dom)
        lines.append("- " + notes[qid].strip().replace("\n", "\n  ") + "\n")
    with open(NOTES_MD, "w") as f:
        f.write("\n".join(lines))

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=HERE, **k)
    def log_message(self, *a):  # quiet
        pass
    def _authorized(self):
        """Localhost always; LAN clients only from private ranges AND with the access-key cookie."""
        try:
            ip = ipaddress.ip_address(self.client_address[0].replace("::ffff:", ""))
        except ValueError:
            return False
        if ip.is_loopback:
            return True
        if not self._lan_ok(ip):
            return False
        c = re.search(r"(?:^|;\s*)ml4t_k=([^;]+)", self.headers.get("Cookie", ""))
        return bool(c) and hmac.compare_digest(c.group(1), LAN_KEY)
    def _lan_ok(self, ip):
        if not (LAN and ip.is_private) or (LAN_ALLOW and str(ip) not in LAN_ALLOW):
            return False
        return LAN_NETS is None or any(ip in n.network for _, n in LAN_NETS)
    def _gate(self):
        """Return True if the request may proceed; otherwise answer it (key link → cookie, or 403)."""
        if self._authorized():
            return True
        q = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query).get("k", [""])[0]
        if LAN and q and hmac.compare_digest(q, LAN_KEY):
            try: ok = self._lan_ok(ipaddress.ip_address(self.client_address[0].replace("::ffff:", "")))
            except ValueError: ok = False
            if ok:
                self.send_response(302); self.send_header("Location", urllib.parse.urlsplit(self.path).path or "/")
                self.send_header("Set-Cookie", f"ml4t_k={LAN_KEY}; Path=/; HttpOnly; SameSite=Strict; Max-Age=2592000")
                self.end_headers(); return False
        body = b"<h3>ML4T study app: not authorized.</h3><p>Open the full link printed in the terminal on the computer running the app (it includes ?k=...).</p>"
        self.send_response(403); self.send_header("Content-Type", "text/html"); self.send_header("Content-Length", str(len(body)))
        self.end_headers(); self.wfile.write(body); return False
    def _is_local(self):
        try: return ipaddress.ip_address(self.client_address[0].replace("::ffff:", "")).is_loopback
        except ValueError: return False
    def _deny(self, code=405):
        self.send_response(code); self.send_header("Content-Length", "0"); self.end_headers()
    do_PUT = do_DELETE = do_PATCH = do_OPTIONS = do_TRACE = do_CONNECT = lambda self: self._deny(405)
    def do_GET(self):
        if not self._gate():
            return
        path = urllib.parse.urlsplit(self.path).path
        if not self._is_local() and path not in REMOTE_GET and not path.startswith("/books/"):
            return self._deny(404)   # remote: only the app page, its data, state, book list, book PDFs
        if path == "/":
            self.path = "/index.html"
        if self.path.split("?")[0] == "/api/state":
            return self._send_json(read_state())
        if self.path.split("?")[0] == "/api/books":   # which PDFs are present (filenames only)
            return self._send_json(sorted(self._books()))
        if self.path.split("?")[0] == "/data.js" and DATA_JS and (self._is_local() or inside_root(DATA_JS)):
            body = open(DATA_JS, "rb").read()
            self.send_response(200); self.send_header("Content-Type", "application/javascript")
            self.send_header("Content-Length", str(len(body))); self.send_header("Cache-Control", "no-store"); self.end_headers()
            self.wfile.write(body); return
        if self.path.startswith("/books/"):
            return self._send_book()
        return super().do_GET()
    def _send_json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200); self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def _books(self):
        return {f for f in os.listdir(BOOKS_DIR) if f.lower().endswith(".pdf")} if os.path.isdir(BOOKS_DIR) else set()
    def _send_book(self):
        """Serve a PDF from BOOKS_DIR by exact filename only (allowlist = current *.pdf in that folder;
        no subpaths, no traversal). Read-only; localhost, or key-authorized LAN clients with --lan."""
        name = urllib.parse.unquote(self.path[len("/books/"):].split("?")[0].split("#")[0])
        allowed = self._books()
        if name not in allowed or "/" in name or "\\" in name:
            self.send_response(404); self.end_headers(); return
        fp = os.path.join(BOOKS_DIR, name)
        if not inside_root(fp):
            self.send_response(404); self.end_headers(); return
        self.send_response(200); self.send_header("Content-Type", "application/pdf")
        self.send_header("Content-Length", str(os.path.getsize(fp)))
        self.send_header("Cache-Control", "private, max-age=3600"); self.end_headers()
        with open(fp, "rb") as f:
            try: shutil.copyfileobj(f, self.wfile, 1 << 20)
            except (BrokenPipeError, ConnectionResetError): pass
    def do_POST(self):
        if not self._gate():
            return
        if self.path.split("?")[0] == "/api/state":
            n = int(self.headers.get("Content-Length", "0"))
            local = self._is_local()
            if n > MAX_POST:
                return self._deny(413)
            try:
                obj = json.loads(self.rfile.read(n) or b"{}")
                if not isinstance(obj, dict):
                    raise ValueError("state must be a JSON object")
                if not local:   # remote: only known study-progress fields, with the expected shapes
                    obj = {k: v for k, v in obj.items() if k in STATE_KEYS}
                    for k in ("notes", "attempts", "seen", "reviewed", "reviewLog", "flagged", "box", "ui"):
                        if k in obj and not isinstance(obj[k], dict):
                            raise ValueError(f"bad field {k}")
                with _lock:   # optimistic concurrency: a save based on an older _rev is merged, not clobbering
                    cur = read_state(); rev = cur.get("_rev", 0); merged = False
                    if cur and (not local or obj.get("_rev", 0) != rev):   # remote saves are ALWAYS additive
                        obj = merge_state(cur, obj); merged = True
                    obj["_rev"] = rev + 1
                    write_state(obj, prune=local)
                return self._send_json({"_rev": obj["_rev"], "merged": merged, **({"state": obj} if merged else {})})
            except Exception as e:
                self.send_response(400); self.end_headers(); self.wfile.write(str(e).encode())
            return
        self.send_response(404); self.end_headers()

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)   # show the startup URLs immediately, even when logged to a file
    os.makedirs(NOTES_DIR, exist_ok=True)
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    if LAN:
        for label, p in (("notes", NOTES_DIR), ("backups", BACKUP_DIR), ("books", BOOKS_DIR), ("data.js", DATA_JS)):
            if p and not inside_root(p):
                sys.exit(f"--lan refused: the {label} path {p} is outside the allowed folder {ROOT} (set ML4T_ROOT).")
        if not os.path.exists(LAN_KEY_FILE):
            alphabet = "abcdefghjkmnpqrstuvwxyz23456789"
            with open(LAN_KEY_FILE, "w") as f: f.write("".join(secrets.choice(alphabet) for _ in range(10)))
            os.chmod(LAN_KEY_FILE, 0o600)
        LAN_KEY = open(LAN_KEY_FILE).read().strip()
    try:
        httpd = socketserver.ThreadingTCPServer(("0.0.0.0" if LAN else "127.0.0.1", PORT), H)
    except OSError:
        sys.exit(f"Port {PORT} is already in use — the app may already be running (open http://127.0.0.1:{PORT}/),\n"
                 f"or start on another port:  ML4T_PORT=8790 python3 app/serve.py --open")
    with httpd:
        url = f"http://127.0.0.1:{PORT}/"
        print(f"ML4T study app → {url}  (Ctrl-C to stop)")
        if LAN:
            ips = [n.ip for _, n in LAN_NETS] if LAN_NETS else ["<this-computer's-Wi-Fi-IP>"]
            for lan_ip in ips:
                print(f"📱 LAN mode ON — on your phone (same Wi-Fi) open:  http://{lan_ip}:{PORT}/?k={LAN_KEY}")
            if LAN_NETS: print("   Accepting devices only from: " + ", ".join(f"{i} {n.network}" for i, n in LAN_NETS))
            print("   Use only on a trusted network (home Wi-Fi). Delete user-data/lan_key.txt to issue a new key.")
            if LAN_ALLOW: print("   Restricted to: " + ", ".join(sorted(LAN_ALLOW)))
        if "--open" in sys.argv: threading.Timer(0.6, lambda: webbrowser.open(url)).start()
        print(f"Notes/progress persist to: {STATE}")
        print(f"Readable notes mirror:     {NOTES_MD}")
        try: httpd.serve_forever()
        except KeyboardInterrupt: print("\nstopped")
