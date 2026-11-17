#!/usr/bin/env python3
"""Rebuild the publish-ready static homepage, RSS feed, and sitemap from tools.json.
No packages required: python3 build.py
"""
from pathlib import Path
from datetime import datetime, timezone
from email.utils import format_datetime
from html import escape
from xml.sax.saxutils import escape as xml_escape
import json
import re

ROOT = Path(__file__).resolve().parent
SITE = 'https://buildiful.github.io'
TOOLS = json.loads((ROOT / 'tools.json').read_text(encoding='utf-8'))
if not TOOLS:
    raise SystemExit('tools.json cannot be empty')
seen_days, seen_slugs = set(), set()
for tool in TOOLS:
    assert isinstance(tool['day'], int) and 1 <= tool['day'] <= 365, 'Invalid day'
    assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', tool['slug']), 'Invalid slug'
    assert tool['kind'] in {'book', 'card', 'gif', 'font', 'music'}, 'Invalid artwork kind (extend build.py for new kinds)'
    assert tool['category'] in {'Create', 'Publish', 'Enjoy'}, 'Invalid category'
    datetime.strptime(tool['date'], '%Y-%m-%d')
    assert tool['day'] not in seen_days and tool['slug'] not in seen_slugs, 'Duplicate day or slug'
    seen_days.add(tool['day']); seen_slugs.add(tool['slug'])
TOOLS.sort(key=lambda item: item['day'], reverse=True)

# Decorative illustrations are original inline SVG and require no external image libraries.
ART = {
  'book': '''<svg viewBox="0 0 220 148" fill="none" aria-hidden="true"><path d="M110 33c-26-20-54-18-80-10v94c29-11 55-9 80 11 24-20 52-22 80-11V23c-27-9-55-10-80 10Z" fill="#f9fdff" stroke="#5384a2" stroke-width="4"/><path d="M110 33v95M46 45c22-6 38-4 52 5M46 62c22-6 38-4 52 5M122 50c15-9 30-11 50-5M122 67c15-9 30-11 50-5" stroke="#91b4c9" stroke-width="4"/><path d="M42 113c19-7 44-8 68 10M178 113c-18-7-46-7-68 10" stroke="#5384a2" stroke-width="3"/></svg>''',
  'card': '''<svg viewBox="0 0 220 148" fill="none" aria-hidden="true"><rect x="36" y="14" width="136" height="107" rx="9" fill="#fff" stroke="#bd7a96" stroke-width="4" transform="rotate(-8 36 14)"/><rect x="57" y="26" width="138" height="101" rx="9" fill="#fffafc" stroke="#c989a5" stroke-width="4"/><path d="M59 101c25-38 45-41 72-18 18 15 33 13 62-18v62H59z" fill="#e8a4b5"/><path d="M59 110c32-32 57-26 81-7 16 13 32 9 53-3v27H59z" fill="#f5d5df"/><circle cx="155" cy="57" r="14" fill="#f4ce81"/><path d="M73 48h37M73 60h24" stroke="#d7a1b4" stroke-width="5"/></svg>''',
  'gif': '''<svg viewBox="0 0 220 148" fill="none" aria-hidden="true"><rect x="29" y="33" width="110" height="87" rx="9" fill="#fff6db" stroke="#cca76b" stroke-width="4"/><rect x="48" y="17" width="114" height="90" rx="9" fill="#fffdf5" stroke="#ccad76" stroke-width="4"/><rect x="67" y="31" width="119" height="86" rx="9" fill="#fff" stroke="#d1aa65" stroke-width="4"/><circle cx="128" cy="69" r="27" fill="#f5cb76"/><path d="M119 54v30l22-15z" fill="#fffaf2"/><path d="M72 133c40 13 82 6 105-10" stroke="#cb9f57" stroke-width="3" stroke-dasharray="6 6"/></svg>''',
  'font': '''<svg viewBox="0 0 220 148" fill="none" aria-hidden="true"><rect x="40" y="20" width="140" height="105" rx="12" fill="#fffaff" stroke="#b29acb" stroke-width="4"/><path d="M59 42h102M59 108h102" stroke="#e6d7f4" stroke-width="3" stroke-dasharray="5 5"/><text x="73" y="96" font-family="Georgia,serif" font-size="76" font-weight="bold" fill="#8362b0">Aa</text><path d="M171 29v15M163 36h16" stroke="#a081c1" stroke-width="3"/></svg>''',
  'music': '''<svg viewBox="0 0 220 148" fill="none" aria-hidden="true"><circle cx="110" cy="73" r="58" fill="#1e4c55" stroke="#468a87" stroke-width="5"/><circle cx="110" cy="73" r="47" stroke="#578d8b" stroke-width="2"/><circle cx="110" cy="73" r="37" stroke="#416f71" stroke-width="2"/><circle cx="110" cy="73" r="24" fill="#b5e5d5" stroke="#6db2ac" stroke-width="4"/><circle cx="110" cy="73" r="5" fill="#28525c"/><path d="M133 57l25-9v34M133 57v34M158 82c0 6-9 9-14 5-5-5 1-12 14-12M133 91c0 6-9 9-14 5-5-5 1-12 14-12" stroke="#edf8f2" stroke-width="4" fill="none"/></svg>'''
}

def make_card(t):
    url=f"{SITE}/{t['slug']}/"
    repo=f"https://github.com/Buildiful/{t['slug']}"
    safe_search=' '.join([t['name'], t['desc'], t['category'], *t['tags']]).lower()
    h=lambda x: escape(str(x),quote=True)
    return f'''<article class="tool-card" data-day="{t['day']}" data-name="{h(t['name'])}" data-category="{t['category']}" data-slug="{t['slug']}" data-search="{h(safe_search)}">
            <div class="tool-art art-{t['kind']}">{ART[t['kind']]}</div>
            <div class="tool-body"><div class="tool-tags"><span class="tool-day">DAY {t['day']:03d}</span><span class="tool-category">{t['category']}</span></div>
            <h3>{h(t['name'])}</h3><p>{h(t['desc'])}</p>
            <div class="tool-card-actions"><a class="tool-open" href="{url}" target="_blank" rel="noopener noreferrer" data-track-tool="{t['slug']}">Open tool <span aria-hidden="true">↗</span></a><a class="tool-code" href="{repo}" target="_blank" rel="noopener noreferrer" data-track-source="{t['slug']}">Source code ↗</a></div></div>
          </article>'''

latest=TOOLS[0]
subs={
  '{{COUNT}}':str(len(TOOLS)), '{{COUNT_PADDED}}':f'{len(TOOLS):03d}',
  '{{LATEST_DAY}}':f'{latest["day"]:03d}', '{{LATEST_NAME}}':escape(latest['name']),
  '{{LATEST_DESC}}':escape(latest['desc']),
  '{{LATEST_URL}}':f'{SITE}/{latest["slug"]}/', '{{LATEST_SLUG}}':latest['slug'],
  '{{LATEST_KIND}}':latest['kind'],
  '{{LATEST_ARTWORK}}': ("""<div class='art-lines art-lines-a'></div><div class='art-lines art-lines-b'></div><div class='record-shadow'></div><div class='record-disc'><div class='record-ring'><div class='record-label'><span>♫</span><span class='record-hole'></span></div></div></div><span class='art-star art-star-a'>✦</span><span class='art-star art-star-b'>✧</span>""" if latest['kind']=='music' else ART[latest['kind']] + "<span class='art-star art-star-a'>✦</span><span class='art-star art-star-b'>✧</span>"),
  '{{TOOL_CARDS}}':'\n          '.join(map(make_card,TOOLS)),
}
html=(ROOT/'template.html').read_text(encoding='utf-8')
for key,value in subs.items():html=html.replace(key,value)
if '{{' in html:raise SystemExit('Unreplaced placeholder found')
(ROOT/'index.html').write_text(html,encoding='utf-8')

items=[]
for t in TOOLS:
    url=f'{SITE}/{t["slug"]}/'
    dt=datetime.strptime(t['date'],'%Y-%m-%d').replace(tzinfo=timezone.utc)
    items.append(f'''    <item><title>{xml_escape(t['name'])} — Day {t['day']:03d}</title><link>{url}</link><guid isPermaLink="true">{url}</guid><description>{xml_escape(t['desc'])}</description><pubDate>{format_datetime(dt,usegmt=True)}</pubDate></item>''')
feed='''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>Buildiful 365 — One Free Tool a Day</title>
  <link>https://buildiful.github.io/</link>
  <description>New free, open-source tools from Buildiful®.</description>
  <language>en-us</language>
'''+'\n'.join(items)+'\n</channel></rss>\n'
(ROOT/'feed.xml').write_text(feed,encoding='utf-8')
urls=['https://buildiful.github.io/','https://buildiful.github.io/privacy.html']+[f'{SITE}/{t["slug"]}/' for t in TOOLS]
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{url}</loc></url>\n' for url in urls)+'</urlset>\n'
(ROOT/'sitemap.xml').write_text(sitemap,encoding='utf-8')
print(f'Built {len(TOOLS)} cards; latest: day {latest["day"]:03d} ({latest["name"]}).')
