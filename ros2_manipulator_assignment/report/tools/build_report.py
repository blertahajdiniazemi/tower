#!/usr/bin/env python3
"""Build Robot_Operating_System_2_Manipulator_Report.docx (and a PDF rendering).

Two passes: the first document is rendered with LibreOffice to measure the page on which
each heading falls; the second pass writes those page numbers into the cached result of the
real TOC field and resolves forward cross-references. Word can refresh all fields (F9).
Usage: python3 build_report.py
"""
import os
import re
import shutil
import subprocess
import sys

import pymupdf as fitz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import content  # noqa: E402
from docx_builder import Report  # noqa: E402
from references import REFS  # noqa: E402

OUT_DIR = os.path.join(content.A, 'report')
NAME = 'Robot_Operating_System_2_Manipulator_Report'


class Citer:
    def __init__(self):
        self.order = []

    def __call__(self, *keys):
        nums = []
        for k in keys:
            if k not in REFS:
                raise KeyError('unknown reference ' + k)
            if k not in self.order:
                self.order.append(k)
            nums.append(self.order.index(k) + 1)
        return ', '.join('[%d]' % n for n in nums)


def build(known_refs=None, toc_pages=None):
    r = Report(known_refs=known_refs, toc_pages=toc_pages)
    cite = Citer()
    # the five note files are cited first so that they are [1]-[5]
    cite('n11', 'n12', 'n13', 'n14', 'n15')
    content.title_page(r)
    content.abstract(r)
    r.toc()
    for section in content.SECTIONS:
        section(r, cite)
    content.references(r, cite.order, REFS)
    r.header_footer('ROS 2: Architecture, Communication and Application in a Manipulator Robot',
                    '[Student Name] · [Module Code]')
    r.finalize_toc()
    r.update_fields_on_open()
    return r, cite


def render_pdf(docx, outdir):
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', outdir, docx],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return os.path.join(outdir, os.path.splitext(os.path.basename(docx))[0] + '.pdf')


def heading_pages(pdf, headings):
    doc = fitz.open(pdf)
    texts = [re.sub(r'\s+', '', pg.get_text()) for pg in doc]
    # body starts after the TOC: find the page with the first numbered heading
    pages = {}
    start = 0
    for level, number, title, _ in headings:
        needle = re.sub(r'\s+', '', ('%s %s' % (number, title)) if number else title)
        found = None
        for k in range(start, len(texts)):
            # skip the TOC pages, which contain every heading followed by dot leaders
            if k < 3 and number:
                continue
            if needle in texts[k]:
                found = k
                break
        if found is None:
            raise RuntimeError('heading not found in PDF: ' + needle)
        pages[title] = found + 1
        start = found
    return pages, len(doc)


def main():
    tmp = os.path.join(OUT_DIR, 'build_tmp')
    os.makedirs(tmp, exist_ok=True)
    r1, cite1 = build()
    p1 = os.path.join(tmp, NAME + '.docx')
    r1.save(p1)
    pages, n1 = heading_pages(render_pdf(p1, tmp), r1.headings)
    r2, cite2 = build(known_refs=r1.refs, toc_pages=pages)
    final = os.path.join(OUT_DIR, NAME + '.docx')
    r2.save(final)
    pdf = render_pdf(final, OUT_DIR)
    pages2, n2 = heading_pages(pdf, r2.headings)
    if pages2 != pages:
        # one more pass if the TOC length changed pagination
        r3, _ = build(known_refs=r2.refs, toc_pages=pages2)
        r3.save(final)
        pdf = render_pdf(final, OUT_DIR)
        pages3, n2 = heading_pages(pdf, r3.headings)
        assert pages3 == pages2, 'TOC page numbers did not converge'
        pages = pages2
    shutil.rmtree(tmp)
    print('pages:', n2)
    for level, number, title, _ in r2.headings:
        print('  %s%s %s .... %s' % ('  ' * (level - 1), number, title, pages.get(title)))
    print('figures', r2.fig_no, 'tables', r2.tab_no, 'listings', r2.lst_no, 'references', len(cite2.order))


if __name__ == '__main__':
    main()
