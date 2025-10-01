import os
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDF_SRC = ROOT / 'pdfs'
DOCS = ROOT / 'docs'
PDF_DST = DOCS / 'pdfs'
COVERS = DOCS / 'covers'
META = DOCS / 'meta.json'

# Ensure folders exist
PDF_DST.mkdir(parents=True, exist_ok=True)
COVERS.mkdir(parents=True, exist_ok=True)

items = []

if not PDF_SRC.exists():
    PDF_SRC.mkdir(parents=True, exist_ok=True)

for p in sorted(PDF_SRC.rglob('*.pdf')):
    rel = p.relative_to(PDF_SRC)
    rel_str = str(rel).replace('\\', '/')

    # Copy PDF to docs/pdfs/
    dst_pdf = PDF_DST / rel
    dst_pdf.parent.mkdir(parents=True, exist_ok=True)
    # Copy only when changed
    if (not dst_pdf.exists()) or (p.stat().st_mtime > dst_pdf.stat().st_mtime) or (p.stat().st_size != dst_pdf.stat().st_size):
        shutil.copy2(p, dst_pdf)

    # Generate cover using pdftoppm (first page)
    rel_no_ext = rel.with_suffix('')
    cover_png = COVERS / (str(rel_no_ext) + '.png')
    cover_png.parent.mkdir(parents=True, exist_ok=True)

    try:
        # If cover missing or older than source, regenerate
        need_gen = (not cover_png.exists()) or (p.stat().st_mtime > cover_png.stat().st_mtime)
        if need_gen:
            # pdftoppm outputs without extension when using -singlefile
            out_prefix = COVERS / str(rel_no_ext)
            out_prefix.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run([
                'pdftoppm', '-f', '1', '-l', '1', '-png', '-singlefile', str(p), str(out_prefix)
            ], check=True)
    except Exception as e:
        # Skip cover generation errors
        pass

    cover_rel = None
    if cover_png.exists():
        cover_rel = './covers/' + str(rel_no_ext).replace('\\', '/') + '.png'

    items.append({
        'name': p.name,
        'path': rel_str,
        'displayPath': str(rel.parent).replace('\\', '/'),
        'url': './pdfs/' + rel_str,
        'cover': cover_rel,
    })

# Sort items by path
items.sort(key=lambda x: x['path'].lower())

META.parent.mkdir(parents=True, exist_ok=True)
with META.open('w', encoding='utf-8') as f:
    json.dump({ 'items': items }, f, ensure_ascii=False, indent=2)

print(f"Wrote {META} with {len(items)} items")
