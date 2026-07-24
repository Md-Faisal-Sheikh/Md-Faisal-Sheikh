#!/usr/bin/env python
"""Generate the custom SVG artwork for the profile README.

Everything is self-contained: no external fonts, no scripts, no remote
refs -- so GitHub renders it through camo without stripping anything.
Animation is SMIL + inline CSS, both of which run inside <img>.
"""
import io, math, os, random

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)

INK = "#e8eefc"
MUTED = "#8aa0c8"


def darken(hexcol, f):
    r = int(hexcol[1:3], 16); g = int(hexcol[3:5], 16); b = int(hexcol[5:7], 16)
    return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))


def write(name, body):
    p = os.path.join(OUT, name)
    io.open(p, "w", encoding="utf-8", newline="\n").write(body)
    print("wrote %-12s %6d bytes" % (name, len(body.encode("utf-8"))))


# ────────────────────────────── hero ──────────────────────────────
def hero():
    W, H = 1000, 340
    HZ = 215                     # horizon
    VPX, VPY = W / 2, HZ
    rnd = random.Random(7)
    o = []

    o.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
             'role="img" aria-label="Md. Faisal Sheikh">' % (W, H, W, H))
    o.append("""<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#04060d"/><stop offset="55%" stop-color="#080f24"/>
  <stop offset="100%" stop-color="#0d1b3f"/>
</linearGradient>
<radialGradient id="glow" cx="50%" cy="100%" r="62%">
  <stop offset="0%" stop-color="#3b82f6" stop-opacity=".55"/>
  <stop offset="55%" stop-color="#1d4ed8" stop-opacity=".13"/>
  <stop offset="100%" stop-color="#000" stop-opacity="0"/>
</radialGradient>
<linearGradient id="face" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#ffffff"/><stop offset="55%" stop-color="#e6edff"/>
  <stop offset="100%" stop-color="#9dc0ff"/>
</linearGradient>
<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#080f24" stop-opacity="1"/>
  <stop offset="100%" stop-color="#080f24" stop-opacity="0"/>
</linearGradient>
<filter id="soft" x="-40%" y="-40%" width="180%" height="180%">
  <feGaussianBlur stdDeviation="7" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
</defs>""")
    o.append('<rect width="%d" height="%d" fill="url(#sky)"/>' % (W, H))
    o.append('<rect width="%d" height="%d" fill="url(#glow)"/>' % (W, H))

    # neural constellation, upper band
    nodes = [(rnd.uniform(60, W - 60), rnd.uniform(26, 104)) for _ in range(22)]
    o.append('<g stroke="#5b8def" stroke-width="1" fill="none" opacity=".30">')
    for i, (x1, y1) in enumerate(nodes):
        for x2, y2 in nodes[i + 1:]:
            if math.hypot(x1 - x2, y1 - y2) < 132:
                o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (x1, y1, x2, y2))
    o.append("</g>")
    o.append('<g fill="#8ab4ff">')
    for i, (x, y) in enumerate(nodes):
        r = rnd.uniform(1.5, 2.9)
        o.append('<circle cx="%.1f" cy="%.1f" r="%.2f" opacity=".85">'
                 '<animate attributeName="opacity" values=".25;.95;.25" dur="%.1fs" '
                 'begin="-%.2fs" repeatCount="indefinite"/></circle>'
                 % (x, y, r, rnd.uniform(2.6, 5.2), rnd.uniform(0, 5)))
    o.append("</g>")

    # perspective floor
    o.append('<g stroke="#4d7fe0" stroke-width="1" opacity=".55">')
    for i in range(-16, 17):
        o.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" opacity=".40"/>'
                 % (VPX, VPY, VPX + i * 105, H))
    N, DUR = 15, 5.6
    ts = [k / 18.0 for k in range(19)]
    for i in range(N):
        ys = ["%.1f" % (HZ + (H - HZ) * (t ** 2.3)) for t in ts]
        op = [".0" if t < .04 else "%.2f" % min(.85, t * 1.7) for t in ts]
        kt = ";".join("%.3f" % t for t in ts)
        o.append('<line x1="0" x2="%d" y1="%s" y2="%s" opacity="0">'
                 '<animate attributeName="y1" values="%s" keyTimes="%s" dur="%.1fs" begin="-%.2fs" repeatCount="indefinite"/>'
                 '<animate attributeName="y2" values="%s" keyTimes="%s" dur="%.1fs" begin="-%.2fs" repeatCount="indefinite"/>'
                 '<animate attributeName="opacity" values="%s" keyTimes="%s" dur="%.1fs" begin="-%.2fs" repeatCount="indefinite"/>'
                 '</line>'
                 % (W, ys[0], ys[0],
                    ";".join(ys), kt, DUR, i * DUR / N,
                    ";".join(ys), kt, DUR, i * DUR / N,
                    ";".join(op), kt, DUR, i * DUR / N))
    o.append("</g>")
    o.append('<rect x="0" y="%d" width="%d" height="46" fill="url(#fade)"/>' % (HZ, W))
    o.append('<line x1="0" y1="%d" x2="%d" y2="%d" stroke="#7fb0ff" stroke-width="1.4" opacity=".75"/>'
             % (HZ, W, HZ))
    o.append('<ellipse cx="%d" cy="%d" rx="230" ry="16" fill="#60a5fa" opacity=".22" filter="url(#soft)"/>'
             % (VPX, HZ))

    # extruded name
    fam = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"
    name = "MD. FAISAL SHEIKH"
    o.append('<g text-anchor="middle" font-family="%s" font-weight="800" font-size="60" letter-spacing="2.5">' % fam)
    for d in range(11, 0, -1):
        o.append('<text x="%.1f" y="%.1f" fill="%s">%s</text>'
                 % (VPX + d * .55, 158 + d * .95, darken("#3b82f6", .30 + .045 * (11 - d)), name))
    o.append('<text x="%d" y="158" fill="url(#face)">%s</text>' % (VPX, name))
    o.append("</g>")

    mono = "ui-monospace,'Cascadia Code','Segoe UI Mono',Consolas,monospace"
    o.append('<text x="%d" y="192" text-anchor="middle" font-family="%s" font-size="14.5" '
             'letter-spacing="4.6" fill="%s">NLP &#183; COMPUTER VISION &#183; MULTIMODAL AI</text>'
             % (VPX, mono, MUTED))
    o.append("</svg>")
    return "\n".join(o)


# ───────────────────────── isometric stack ─────────────────────────
LAYERS = [
    ("INFRASTRUCTURE", "Docker  ·  Git  ·  GitHub Actions  ·  Linux", "#7c3aed"),
    ("DATA",           "MongoDB  ·  Supabase  ·  Postgres  ·  SQLite", "#6366f1"),
    ("BACKEND",        "FastAPI  ·  Node.js  ·  Express",              "#3b82f6"),
    ("FRONTEND",       "React  ·  Next.js  ·  Vite  ·  Tailwind",      "#0ea5e9"),
    ("AI / ML",        "PyTorch  ·  scikit-learn  ·  Hugging Face",    "#22d3ee"),
]


def stack():
    W, H = 960, 560
    SZ, TH, GAP = 214, 30, 24
    CX, CY = 292, 306
    iso = lambda x, y, z: (CX + (x - y) * 0.866, CY + (x + y) * 0.5 - z)
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
         'role="img" aria-label="Isometric view of the stack, infrastructure through AI and ML">' % (W, H, W, H)]
    o.append("""<defs>
<filter id="sh" x="-30%" y="-30%" width="160%" height="160%">
  <feDropShadow dx="0" dy="7" stdDeviation="9" flood-color="#000" flood-opacity=".55"/>
</filter>
<radialGradient id="pool" cx="50%" cy="50%" r="50%">
  <stop offset="0%" stop-color="#3b82f6" stop-opacity=".30"/>
  <stop offset="100%" stop-color="#3b82f6" stop-opacity="0"/>
</radialGradient>
</defs>""")
    o.append('<rect width="%d" height="%d" fill="#0a0f1e"/>' % (W, H))
    o.append('<ellipse cx="%d" cy="%d" rx="250" ry="82" fill="url(#pool)"/>' % (CX, CY + 128))

    mono = "ui-monospace,'Cascadia Code','Segoe UI Mono',Consolas,monospace"
    fam = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"

    for k, (title, items, col) in enumerate(LAYERS):
        z0 = k * (TH + GAP)
        z1 = z0 + TH
        top = [iso(0, 0, z1), iso(SZ, 0, z1), iso(SZ, SZ, z1), iso(0, SZ, z1)]
        right = [iso(SZ, 0, z1), iso(SZ, SZ, z1), iso(SZ, SZ, z0), iso(SZ, 0, z0)]
        left = [iso(0, SZ, z1), iso(SZ, SZ, z1), iso(SZ, SZ, z0), iso(0, SZ, z0)]
        pts = lambda P: " ".join("%.1f,%.1f" % p for p in P)

        o.append('<g filter="url(#sh)">')
        o.append('<animateTransform attributeName="transform" type="translate" '
                 'values="0 0; 0 -7; 0 0" dur="5.2s" begin="-%.2fs" repeatCount="indefinite" '
                 'calcMode="spline" keySplines=".4 0 .6 1;.4 0 .6 1" keyTimes="0;0.5;1"/>' % (k * 0.55))
        o.append('<polygon points="%s" fill="%s"/>' % (pts(left), darken(col, .46)))
        o.append('<polygon points="%s" fill="%s"/>' % (pts(right), darken(col, .68)))
        o.append('<polygon points="%s" fill="%s"/>' % (pts(top), col))
        o.append('<polygon points="%s" fill="none" stroke="#dbeafe" stroke-opacity=".30" stroke-width="1"/>' % pts(top))

        # connector + labels
        ax, ay = iso(SZ, 0, z1)
        lx = 566
        o.append('<path d="M%.1f %.1f L%.1f %.1f L%.1f %.1f" fill="none" stroke="%s" '
                 'stroke-width="1.3" opacity=".85"/>' % (ax + 4, ay + 6, ax + 40, ay - 12, lx - 12, ay - 12, col))
        o.append('<circle cx="%.1f" cy="%.1f" r="3" fill="%s"/>' % (ax + 4, ay + 6, col))
        o.append('<text x="%d" y="%.1f" font-family="%s" font-size="19" font-weight="800" '
                 'letter-spacing="1.6" fill="%s">%s</text>' % (lx, ay - 8, fam, col, title))
        o.append('<text x="%d" y="%.1f" font-family="%s" font-size="12.5" fill="%s">%s</text>'
                 % (lx, ay + 12, mono, MUTED, items))
        o.append("</g>")

    o.append("</svg>")
    return "\n".join(o)


# ───────────────────────────── footer ─────────────────────────────
def footer():
    W, H = 1000, 130
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d" '
         'role="img" aria-label="">' % (W, H, W, H)]
    o.append("""<defs>
<linearGradient id="fg" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0%" stop-color="#0d1b3f"/><stop offset="100%" stop-color="#04060d"/>
</linearGradient>
<linearGradient id="rule" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0%" stop-color="#3b82f6" stop-opacity="0"/>
  <stop offset="50%" stop-color="#7fb0ff" stop-opacity=".95"/>
  <stop offset="100%" stop-color="#3b82f6" stop-opacity="0"/>
</linearGradient>
</defs>""")
    o.append('<rect width="%d" height="%d" fill="url(#fg)"/>' % (W, H))
    o.append('<g stroke="#4d7fe0" stroke-width="1" opacity=".28">')
    for i in range(-16, 17):
        o.append('<line x1="%d" y1="%d" x2="%.1f" y2="0"/>' % (W // 2, H, W / 2 + i * 105))
    o.append("</g>")
    o.append('<rect x="0" y="0" width="%d" height="2" fill="url(#rule)"/>' % W)
    mono = "ui-monospace,'Cascadia Code','Segoe UI Mono',Consolas,monospace"
    o.append('<text x="%d" y="74" text-anchor="middle" font-family="%s" font-size="13" '
             'letter-spacing="3.4" fill="%s">BUILDING SYSTEMS THAT READ, SEE AND REASON</text>'
             % (W // 2, mono, MUTED))
    o.append("</svg>")
    return "\n".join(o)


write("hero.svg", hero())
write("stack.svg", stack())
write("footer.svg", footer())
