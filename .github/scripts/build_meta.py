import os
import json
import shutil
import subprocess
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
PDF_SRC = ROOT / 'pdfs'
DOCS = ROOT / 'docs'
PDF_DST = DOCS / 'pdfs'
COVERS = DOCS / 'covers'
META = DOCS / 'meta.json'

# Ensure folders exist
PDF_DST.mkdir(parents=True, exist_ok=True)
COVERS.mkdir(parents=True, exist_ok=True)

# Limit cover max dimension for performance
MAX_DIM = os.environ.get('COVER_MAX_DIM', '1024')  # longest side in px
JPEG_QUALITY = os.environ.get('COVER_JPEG_QUALITY', '85')

STOPWORDS = set(['the','and','of','to','in','for','on','a','an','with','at','by','from','is','are','this','that','pdf','v','ver','rev','edition','ed','vol','part','chap','chapter','notes','book'])
CH_SEP = re.compile(r"[\s_\-\.\[\]\(\)/]+")

items = []

if not PDF_SRC.exists():
    PDF_SRC.mkdir(parents=True, exist_ok=True)


def parse_pdfinfo(path: Path):
    title = None
    author = None
    pages = None
    try:
        out = subprocess.check_output(['pdfinfo', str(path)], text=True, stderr=subprocess.STDOUT)
        for line in out.splitlines():
            if line.startswith('Title:'):
                title = line.split(':', 1)[1].strip() or None
            elif line.startswith('Author:'):
                author = line.split(':', 1)[1].strip() or None
            elif line.startswith('Pages:'):
                try:
                    pages = int(line.split(':', 1)[1].strip())
                except Exception:
                    pages = None
    except Exception:
        pass
    return title, author, pages


def build_tags(name: str, rel: Path):
    tokens = []
    stem = Path(name).stem
    tokens.extend([t for t in CH_SEP.split(stem) if t])
    for seg in rel.parent.parts:
        tokens.extend([t for t in CH_SEP.split(seg) if t])
    norm = []
    for t in tokens:
        s = t.strip().lower()
        if not s:
            continue
        if s in STOPWORDS:
            continue
        if len(s) <= 1:
            continue
        norm.append(s)
    seen = set()
    res = []
    for t in norm:
        if t not in seen:
            seen.add(t)
            res.append(t)
    return res[:20]

for p in sorted(PDF_SRC.rglob('*.pdf')):
    rel = p.relative_to(PDF_SRC)
    rel_str = str(rel).replace('\\', '/')

    dst_pdf = PDF_DST / rel
    dst_pdf.parent.mkdir(parents=True, exist_ok=True)
    if (not dst_pdf.exists()) or (p.stat().st_mtime > dst_pdf.stat().st_mtime) or (p.stat().st_size != dst_pdf.stat().st_size):
        shutil.copy2(p, dst_pdf)

    title, author, pages = parse_pdfinfo(p)
    size_bytes = p.stat().st_size
    mtime = int(p.stat().st_mtime)
    tags = build_tags(p.name, rel)

    rel_no_ext = rel.with_suffix('')
    cover_png = COVERS / (str(rel_no_ext) + '.png')
    cover_jpg = COVERS / (str(rel_no_ext) + '.jpg')
    cover_file = None

    try:
        need_gen = True
        if cover_jpg.exists():
            cover_file = cover_jpg
            need_gen = p.stat().st_mtime > cover_jpg.stat().st_mtime
        elif cover_png.exists():
            cover_file = cover_png
            need_gen = p.stat().st_mtime > cover_png.stat().st_mtime

        if need_gen:
            out_prefix = COVERS / str(rel_no_ext)
            out_prefix.parent.mkdir(parents=True, exist_ok=True)
            try:
                subprocess.run([
                    'pdftoppm', '-f', '1', '-l', '1', '-jpeg', '-jpegopt', f'quality={JPEG_QUALITY}', '-singlefile', '-scale-to', str(MAX_DIM), str(p), str(out_prefix)
                ], check=True)
                cover_file = cover_jpg
            except Exception:
                subprocess.run([
                    'pdftoppm', '-f', '1', '-l', '1', '-png', '-singlefile', '-scale-to', str(MAX_DIM), str(p), str(out_prefix)
                ], check=True)
                cover_file = cover_png
    except Exception:
        cover_file = None

    cover_rel = None
    if cover_file and cover_file.exists():
        cover_rel = '/covers/' + str(rel_no_ext).replace('\\', '/') + cover_file.suffix

    items.append({
        'id': rel_str,
        'name': p.name,
        'title': title or Path(p.name).stem,
        'author': author,
        'pages': pages,
        'size': size_bytes,
        'mtime': mtime,
        'tags': tags,
        'path': rel_str,
        'displayPath': str(rel.parent).replace('\\', '/'),
        'url': '/pdfs/' + rel_str,
        'cover': cover_rel,
    })

items.sort(key=lambda x: x['path'].lower())

META.parent.mkdir(parents=True, exist_ok=True)
with META.open('w', encoding='utf-8') as f:
    json.dump({ 'items': items }, f, ensure_ascii=False, indent=2)

print(f"Wrote {META} with {len(items)} items")
