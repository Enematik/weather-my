#!/usr/bin/env python3
"""Erzeugt die App-Icons (icon-512.png, icon-192.png, apple-touch-icon.png).
Reine Standardbibliothek (zlib, struct, math) - keine Zusatzpakete nötig.
Aufruf im Ordner der App:  python make_icons.py
"""
import zlib, struct, math, os, tempfile

C1 = (30, 110, 210)      # Gradient oben-links
C2 = (15, 35, 80)        # Gradient unten-rechts
WHITE = (245, 250, 255)  # Wolke
DROP = (120, 205, 245)   # Regentropfen

# Design in 512x512-Referenzkoordinaten
ELLIPSES = [(200, 230, 90, 90), (310, 210, 100, 100), (405, 245, 75, 75)]
RECT = (110, 240, 480, 350)
LINES = [((165, 300), (140, 400)), ((250, 300), (225, 400)), ((335, 300), (310, 400))]
STROKE = 14.0

def in_cloud(x, y):
    for cx, cy, rx, ry in ELLIPSES:
        dx = (x - cx) / rx
        dy = (y - cy) / ry
        if dx * dx + dy * dy <= 1.0:
            return True
    x1, y1, x2, y2 = RECT
    return x1 <= x <= x2 and y1 <= y <= y2

def seg_dist(px, py, a, b):
    (x1, y1), (x2, y2) = a, b
    dx, dy = x2 - x1, y2 - y1
    L2 = dx * dx + dy * dy
    t = ((px - x1) * dx + (py - y1) * dy) / L2
    if t < 0:
        t = 0.0
    elif t > 1:
        t = 1.0
    cx, cy = x1 + t * dx, y1 + t * dy
    return math.hypot(px - cx, py - cy)

def grad(x, y):
    t = (x + y) / 1024.0
    return (int(C1[0] + (C2[0] - C1[0]) * t),
            int(C1[1] + (C2[1] - C1[1]) * t),
            int(C1[2] + (C2[2] - C1[2]) * t))

def make_icon(size):
    S = 3  # 3x Supersampling für glatte Kanten
    img = []
    for oy in range(size):
        row = []
        for ox in range(size):
            nw = nd = n = 0
            for sy in range(S):
                for sx in range(S):
                    x = (ox + (sx + 0.5) / S) * 512.0 / size
                    y = (oy + (sy + 0.5) / S) * 512.0 / size
                    n += 1
                    if in_cloud(x, y):
                        nw += 1
                    elif any(seg_dist(x, y, a, b) <= STROKE / 2 for a, b in LINES):
                        nd += 1
            bg = grad(ox + 0.5, oy + 0.5)
            cw = nw / n
            cd = nd / n
            row.append(tuple(int(bg[i] * (1 - cw - cd) + WHITE[i] * cw + DROP[i] * cd) for i in range(3)))
        img.append(row)
    return png(size, size, img)

def png(width, height, pixels):
    raw = bytearray()
    for row in pixels:
        raw.append(0)
        for px in row:
            raw.extend(px)
    def chunk(t, d):
        body = t + d
        return struct.pack('>I', len(d)) + body + struct.pack('>I', zlib.crc32(body) & 0xffffffff)
    out = b'\x89PNG\r\n\x1a\n'
    out += chunk(b'IHDR', struct.pack('>IIBBBBB', width, height, 8, 2, 0, 0, 0))
    out += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    out += chunk(b'IEND', b'')
    return out

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    out_dir = base
    try:  # Prüfen, ob der App-Ordner beschreibbar ist
        probe = os.path.join(base, '_probe.tmp')
        with open(probe, 'wb') as f:
            f.write(b'x')
        os.remove(probe)
    except OSError:
        out_dir = tempfile.gettempdir()
        print('Hinweis: Der App-Ordner ist hier nicht beschreibbar, '
              'die Icons kommen in den Temp-Ordner.')
    written = []
    for fname, size in [('icon-512.png', 512), ('icon-192.png', 192), ('apple-touch-icon.png', 180)]:
        path = os.path.join(out_dir, fname)
        with open(path, 'wb') as f:
            f.write(make_icon(size))
        written.append(path)
        print('wrote', path)
    if out_dir != base:
        print('-> Kopiere die drei PNG-Dateien aus %s in %s (Explorer: hin- und herziehen).' % (out_dir, base))
        print('   Oder in einem normalen Terminal:')
        print('   copy %s\\icon-512.png %s\\' % (out_dir, base))
        print('   copy %s\\icon-192.png %s\\' % (out_dir, base))
        print('   copy %s\\apple-touch-icon.png %s\\' % (out_dir, base))

if __name__ == '__main__':
    main()
