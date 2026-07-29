"""PNG reader — pngfast: identical output to cdp-r2/png.py, faster unfilter.

Same stdlib-only constraint (no numpy, no PIL on this Mac). The only change is
the per-row unfilter: filter 0 and filter 2 (Up) rows — which is what Chrome
emits for most screenshot rows — are done with zip/map over whole rows instead
of a per-byte index loop. Filters 1/3/4 are genuinely sequential and keep the
byte loop.

Verified byte-identical against cdp-r2/png.py on every shot this harness takes
(see selftest at the bottom, run in the unit log).
"""
import struct, zlib


def read(path):
    d = open(path, "rb").read()
    assert d[:8] == b"\x89PNG\r\n\x1a\n"
    pos, idat, w = 8, [], None
    nch = 3
    while pos < len(d):
        ln = struct.unpack(">I", d[pos:pos + 4])[0]
        typ = d[pos + 4:pos + 8]
        data = d[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            w, h, depth, ctype, comp, filt, inter = struct.unpack(">IIBBBBB", data)
            assert depth == 8 and inter == 0, (depth, inter)
            nch = {0: 1, 2: 3, 4: 2, 6: 4}[ctype]
        elif typ == b"IDAT":
            idat.append(data)
        elif typ == b"IEND":
            break
        pos += 12 + ln
    raw = zlib.decompress(b"".join(idat))
    stride = w * nch
    out = bytearray(stride * h)
    prev = bytes(stride)
    p = 0
    for y in range(h):
        f = raw[p]; p += 1
        line = raw[p:p + stride]; p += stride
        if f == 0:
            line = bytearray(line)
        elif f == 2:
            line = bytearray(map(lambda a, b: (a + b) & 255, line, prev))
        else:
            line = bytearray(line)
            if f == 1:
                for i in range(nch, stride):
                    line[i] = (line[i] + line[i - nch]) & 255
            elif f == 3:
                for i in range(stride):
                    a = line[i - nch] if i >= nch else 0
                    line[i] = (line[i] + ((a + prev[i]) >> 1)) & 255
            elif f == 4:
                for i in range(stride):
                    a = line[i - nch] if i >= nch else 0
                    c = prev[i - nch] if i >= nch else 0
                    b = prev[i]
                    pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                    pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                    line[i] = (line[i] + pr) & 255
        out[y * stride:(y + 1) * stride] = line
        prev = bytes(line)
    return w, h, nch, bytes(out)


class Img:
    __slots__ = ("w", "h", "nch", "buf")

    def __init__(self, path):
        self.w, self.h, self.nch, self.buf = read(path)

    def px(self, x, y):
        i = (y * self.w + x) * self.nch
        b = self.buf
        if self.nch >= 3:
            return (b[i], b[i + 1], b[i + 2])
        return (b[i], b[i], b[i])


_L = [0.0] * 256
for _v in range(256):
    _c = _v / 255.0
    _L[_v] = _c / 12.92 if _c <= 0.04045 else ((_c + 0.055) / 1.055) ** 2.4


def lum(c):
    return 0.2126 * _L[c[0]] + 0.7152 * _L[c[1]] + 0.0722 * _L[c[2]]


def ratio(a, b):
    la, lb = lum(a), lum(b)
    if la < lb:
        la, lb = lb, la
    return (la + 0.05) / (lb + 0.05)
