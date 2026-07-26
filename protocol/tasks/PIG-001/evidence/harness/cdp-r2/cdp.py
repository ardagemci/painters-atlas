"""Minimal pure-stdlib Chrome DevTools Protocol client (Vermeer evidence harness).

No third-party packages exist on this Mac (no node, no websocket-client, no PIL),
so this implements RFC6455 client framing directly over a localhost socket.
Used because headless Chrome's --window-size is clamped to a 500px minimum on
macOS, which silently produced 500px-wide layouts cropped to 390px files.
Emulation.setDeviceMetricsOverride is not subject to that clamp.
"""
import base64, hashlib, json, os, random, socket, struct, subprocess, sys, time
import urllib.request

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


class WS:
    def __init__(self, url):
        # ws://127.0.0.1:PORT/path
        rest = url[len("ws://"):]
        hostport, _, path = rest.partition("/")
        host, _, port = hostport.partition(":")
        self.sock = socket.create_connection((host, int(port)))
        self.sock.settimeout(60)
        key = base64.b64encode(os.urandom(16)).decode()
        req = (
            "GET /%s HTTP/1.1\r\nHost: %s\r\nUpgrade: websocket\r\n"
            "Connection: Upgrade\r\nSec-WebSocket-Key: %s\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n" % (path, hostport, key)
        )
        self.sock.sendall(req.encode())
        buf = b""
        while b"\r\n\r\n" not in buf:
            buf += self.sock.recv(4096)
        head, _, tail = buf.partition(b"\r\n\r\n")
        assert b"101" in head.split(b"\r\n")[0], head
        self.buf = tail

    def _read(self, n):
        while len(self.buf) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise IOError("socket closed")
            self.buf += chunk
        out, self.buf = self.buf[:n], self.buf[n:]
        return out

    def send(self, text):
        payload = text.encode()
        n = len(payload)
        hdr = bytearray([0x81])
        if n < 126:
            hdr.append(0x80 | n)
        elif n <= 0xFFFF:
            hdr.append(0x80 | 126)
            hdr += struct.pack(">H", n)
        else:
            hdr.append(0x80 | 127)
            hdr += struct.pack(">Q", n)
        mask = os.urandom(4)
        hdr += mask
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(bytes(hdr) + masked)

    def recv(self):
        """Return one complete text message (reassembling fragments)."""
        parts = []
        while True:
            b0, b1 = self._read(2)
            fin = b0 & 0x80
            op = b0 & 0x0F
            ln = b1 & 0x7F
            if ln == 126:
                ln = struct.unpack(">H", self._read(2))[0]
            elif ln == 127:
                ln = struct.unpack(">Q", self._read(8))[0]
            data = self._read(ln) if ln else b""
            if op == 0x9:  # ping -> pong
                self.sock.sendall(b"\x8a\x80" + os.urandom(4))
                continue
            if op == 0x8:
                raise IOError("websocket closed by peer")
            if op == 0xA:
                continue
            parts.append(data)
            if fin:
                return b"".join(parts).decode("utf-8", "replace")

    def close(self):
        try:
            self.sock.close()
        except Exception:
            pass


class Browser:
    def __init__(self, port=9333, headless=True):
        self.port = port
        prof = "/tmp/vermeer-cdp-%d" % port
        subprocess.run(["rm", "-rf", prof])
        args = [
            CHROME, "--remote-debugging-port=%d" % port,
            "--user-data-dir=" + prof, "--no-first-run", "--no-default-browser-check",
            "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
            "--disable-background-timer-throttling",
            "--disable-renderer-backgrounding",
            "--disable-backgrounding-occluded-windows",
            "--window-size=1600,1000", "about:blank",
        ]
        if headless:
            args.insert(1, "--headless=new")
        self.proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ws_url = None
        for _ in range(80):
            try:
                v = json.load(urllib.request.urlopen("http://127.0.0.1:%d/json/version" % port, timeout=2))
                ws_url = v["webSocketDebuggerUrl"]
                break
            except Exception:
                time.sleep(0.25)
        if not ws_url:
            raise RuntimeError("Chrome did not expose a CDP endpoint")
        self.browser_ws = WS(ws_url)
        self._id = 0
        # create a page target
        tid = self._bcmd("Target.createTarget", {"url": "about:blank"})["targetId"]
        self.target_id = tid
        tgts = json.load(urllib.request.urlopen("http://127.0.0.1:%d/json/list" % port, timeout=5))
        page = [t for t in tgts if t.get("id") == tid][0]
        self.ws = WS(page["webSocketDebuggerUrl"])
        self.events = []
        self.cmd("Page.enable")
        self.cmd("Runtime.enable")
        self.cmd("Network.enable")
        self.cmd("Log.enable")
        self.cmd("Network.setCacheDisabled", {"cacheDisabled": True})

    def _bcmd(self, method, params=None):
        self._id += 1
        i = self._id
        self.browser_ws.send(json.dumps({"id": i, "method": method, "params": params or {}}))
        while True:
            m = json.loads(self.browser_ws.recv())
            if m.get("id") == i:
                if "error" in m:
                    raise RuntimeError("%s: %s" % (method, m["error"]))
                return m.get("result", {})

    def cmd(self, method, params=None, timeout=60):
        self._id += 1
        i = self._id
        self.ws.send(json.dumps({"id": i, "method": method, "params": params or {}}))
        t0 = time.time()
        while True:
            m = json.loads(self.ws.recv())
            if "id" in m:
                if m["id"] == i:
                    if "error" in m:
                        raise RuntimeError("%s: %s" % (method, m["error"]))
                    return m.get("result", {})
            else:
                self.events.append(m)
            if time.time() - t0 > timeout:
                raise TimeoutError(method)

    def drain(self, seconds=0.0):
        """Collect pending events without issuing a command."""
        end = time.time() + seconds
        self.ws.sock.settimeout(0.2)
        try:
            while time.time() < end:
                try:
                    m = json.loads(self.ws.recv())
                except socket.timeout:
                    continue
                except IOError:
                    break
                if "id" not in m:
                    self.events.append(m)
        finally:
            self.ws.sock.settimeout(60)

    def metrics(self, w, h, mobile=False, dsf=1):
        self.cmd("Emulation.setDeviceMetricsOverride",
                 {"width": w, "height": h, "deviceScaleFactor": dsf, "mobile": mobile})

    def goto(self, url, settle=1.4):
        self.cmd("Page.navigate", {"url": url})
        # wait for load event
        t0 = time.time()
        seen = False
        self.ws.sock.settimeout(0.4)
        try:
            while time.time() - t0 < 25:
                try:
                    m = json.loads(self.ws.recv())
                except socket.timeout:
                    if seen:
                        break
                    continue
                except IOError:
                    break
                if "id" not in m:
                    self.events.append(m)
                    if m.get("method") == "Page.loadEventFired":
                        seen = True
                        break
        finally:
            self.ws.sock.settimeout(60)
        time.sleep(settle)

    def ev(self, expr, await_promise=False):
        r = self.cmd("Runtime.evaluate",
                     {"expression": expr, "returnByValue": True,
                      "awaitPromise": await_promise, "allowUnsafeEvalBlockedByCSP": True})
        if r.get("exceptionDetails"):
            raise RuntimeError(json.dumps(r["exceptionDetails"])[:900])
        return r["result"].get("value")

    def shot(self, path):
        r = self.cmd("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": False})
        with open(path, "wb") as f:
            f.write(base64.b64decode(r["data"]))
        return os.path.getsize(path)

    def close(self):
        try:
            self.ws.close(); self.browser_ws.close()
        except Exception:
            pass
        self.proc.terminate()
        try:
            self.proc.wait(timeout=8)
        except Exception:
            self.proc.kill()


BASE = "http://localhost:8421"

ROUTES16 = [
    ("home", "#/"), ("artists", "#/artists"), ("artist-leonardo", "#/artist/leonardo-da-vinci"),
    ("artwork-david", "#/artwork/david"), ("explore", "#/explore"), ("timeline", "#/timeline"),
    ("influences", "#/influences"), ("museums", "#/museums"), ("museum-louvre", "#/museum/louvre"),
    ("lists", "#/lists"), ("palette", "#/palette"), ("taste", "#/taste"), ("daily", "#/daily"),
    ("privacy", "#/privacy"), ("credits", "#/credits"), ("invalid-route", "#/no-such-page"),
]


def set_theme(b, theme):
    b.goto(BASE + "/index.html", settle=0.3)
    b.ev("localStorage.setItem('pigment-theme',%r)" % theme)
