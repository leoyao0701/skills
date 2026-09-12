#!/usr/bin/env python3
"""Extract PDF text with PDF-page locators; optional Tesseract OCR, never marked verified."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess


def selected_pages(spec, count):
    result = set()
    for part in spec.split(','):
        bounds = part.strip().split('-')
        if len(bounds) > 2:
            raise ValueError('页码格式如 1,3-5。')
        start = int(bounds[0]); end = int(bounds[-1])
        if start < 1 or end > count or end < start:
            raise ValueError(f'页码需位于 1—{count}，且范围顺序正确。')
        result.update(range(start, end + 1))
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pdf', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--ocr-pages', help='要 OCR 的 PDF 页号，如 1,3-5；省略时仅提取文本')
    ap.add_argument('--language', default='chi_sim+eng')
    args = ap.parse_args()
    if args.pdf.resolve() == args.out.resolve():
        raise SystemExit('输出不能覆盖输入 PDF。')
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit('需要 pypdf；请安装 scripts/requirements-pdf.txt。') from exc
    reader = PdfReader(args.pdf)
    chosen = selected_pages(args.ocr_pages, len(reader.pages)) if args.ocr_pages else set()
    doc = None
    if chosen:
        binary = shutil.which('tesseract')
        if not binary:
            raise SystemExit('未找到 Tesseract。请单独安装程序和所需语言包，或省略 --ocr-pages。')
        try:
            import pypdfium2 as pdfium
        except ImportError as exc:
            raise SystemExit('OCR 页图渲染需要 pypdfium2 和 Pillow。') from exc
        doc = pdfium.PdfDocument(str(args.pdf))
    pages = []
    try:
        for n, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ''
            item = {'pdf_page': n, 'printed_page': None, 'method': 'embedded_text',
                    'review_status': 'not_verified', 'text': text}
            if n in chosen:
                image_dir = args.out.parent / (args.out.stem + '-pages')
                image_dir.mkdir(parents=True, exist_ok=True)
                image_path = image_dir / f'{n:04d}.png'
                source_page = doc[n - 1]
                bitmap = source_page.render(scale=2)
                try:
                    bitmap.to_pil().save(image_path)
                finally:
                    bitmap.close(); source_page.close()
                process = subprocess.run([binary, str(image_path), 'stdout', '-l', args.language],
                                         capture_output=True, text=True, encoding='utf-8')
                if process.returncode:
                    raise RuntimeError(f'第 {n} 页 OCR 失败：{process.stderr.strip()}')
                item.update(method='tesseract_ocr', text=process.stdout,
                            page_image=str(image_path.relative_to(args.out.parent)))
            if not item['text'].strip():
                item['warning'] = '未提取到文字，不能据此认为原页没有内容。'
            pages.append(item)
    finally:
        if doc is not None:
            doc.close()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({'source_name': args.pdf.name, 'page_count': len(pages),
                                   'note': 'pdf_page 为从 1 开始的 PDF 页号，不等于印刷页。所有文本仍需回看原页核查。',
                                   'pages': pages}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'已提取 {len(pages)} 页；OCR {len(chosen)} 页。尚未核查原文。')


if __name__ == '__main__':
    main()
