#!/usr/bin/env python3
"""Check generated HTML in Chromium and save screenshots; not a source-accuracy audit."""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('html', type=Path)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--browser-executable', help='可选：使用已有的兼容 Chromium 浏览器可执行文件')
    args = ap.parse_args()
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise SystemExit('需要 Playwright；安装 playwright 并运行 python -m playwright install chromium。') from exc
    args.out.mkdir(parents=True, exist_ok=True)
    findings, pages, runtime_errors = [], [], []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(executable_path=args.browser_executable)
        page = browser.new_page(viewport={'width': 1600, 'height': 1100}, device_scale_factor=1)
        page.on('pageerror', lambda error: runtime_errors.append(str(error)))
        page.goto(args.html.resolve().as_uri(), wait_until='load')
        page.evaluate('document.fonts.ready')
        count = page.locator('.slide').count()
        if not count:
            raise RuntimeError('没有找到 .slide，输入应为本工具生成的演示 HTML。')
        for i in range(count):
            page.evaluate('(n) => document.querySelectorAll(".slide").forEach((e,i) => e.hidden=i!==n)', i)
            slide = page.locator('.slide').nth(i)
            result = slide.evaluate('''root => {
                const bad=[]; const rb=root.getBoundingClientRect();
                for(const el of root.querySelectorAll('h1,h3,p,blockquote,td,th,.component')) {
                    const r=el.getBoundingClientRect();
                    if(el.scrollWidth>el.clientWidth+2 || el.scrollHeight>el.clientHeight+2 || r.right>rb.right+2 || r.left<rb.left-2)
                        bad.push({tag:el.tagName,text:el.textContent.slice(0,100)});
                }
                return {id:root.id,width:rb.width,height:rb.height,overflow:bad};
            }''')
            slide.screenshot(path=str(args.out / f'{i+1:03d}.png'))
            pages.append(result)
            if result['overflow']:
                findings.append({'page': i+1, 'issue': '元素出现溢出，请查看截图。'})
        browser.close()
    report = {'pages': pages, 'findings': findings, 'runtime_errors': runtime_errors,
              'scope': 'Chromium 指定视口中的溢出与脚本错误，以及截图留存；不验证所有重叠、字体一致性、PPTX 或学术准确性。'}
    (args.out / 'render-check.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'pages': count, 'findings': len(findings), 'runtime_errors': runtime_errors}, ensure_ascii=False))
    if findings or runtime_errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
