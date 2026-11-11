"""Gera o PDF do site a partir do index.html.

Uso: python scripts/make_pdf.py index.html pamella-carneiro-cv.pdf
Roda automaticamente pelo GitHub Actions (.github/workflows/pdf.yml).
"""
import os
import pathlib
import sys

from playwright.sync_api import sync_playwright

src = pathlib.Path(sys.argv[1]).resolve()
out = sys.argv[2]

with sync_playwright() as p:
    opts = {"args": ["--no-sandbox"]}
    if os.environ.get("CHROME_PATH"):
        opts["executable_path"] = os.environ["CHROME_PATH"]
    browser = p.chromium.launch(**opts)
    page = browser.new_page()
    page.goto(src.as_uri())
    page.wait_for_load_state("networkidle")   # espera as fontes carregarem
    page.wait_for_timeout(800)
    page.emulate_media(media="print", color_scheme="light")
    page.pdf(path=out, format="A4", print_background=True, prefer_css_page_size=True)
    browser.close()

print(f"PDF gerado: {out}")
