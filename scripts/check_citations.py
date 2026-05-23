#!/usr/bin/env python3
"""Verify all 30 references cited, with per-chapter breakdown."""
import re

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# Split body and reference section
ref_start = content.find(r'\section*{参考文献}')
body = content[:ref_start]
ref_section = content[ref_start:]

# Split into chapters
ch_titles = ['绪论', '相关技术', '需求分析与系统设计', '关键模块实现', '系统测试与评测', '结论与展望']
ch_pattern = r'\\section\{(' + '|'.join(re.escape(t) for t in ch_titles) + ')\}'

ch_starts = [(m.group(1), m.start()) for m in re.finditer(ch_pattern, body)]
ch_starts.append(('END', len(body)))

chapters = {}
for i, (title, start) in enumerate(ch_starts[:-1]):
    end = ch_starts[i+1][1]
    chapters[title] = body[start:end]

def find_citations(text):
    nums = set()
    for m in re.finditer(r'textsuperscript\{\[([0-9,\s]+)\]\}', text):
        for n in m.group(1).split(','):
            nums.add(int(n.strip()))
    return nums

# Overall
all_cited = find_citations(body)
print(f'Total unique refs cited: {len(all_cited)} / 30')
print(f'Cited: {sorted(all_cited)}')
uncited = sorted(set(range(1, 31)) - all_cited)
if uncited:
    print(f'*** UNCITED: {uncited} ***')
else:
    print('All 30 references are cited in body text.')

# Per chapter
print('\n=== Per-Chapter Breakdown ===')
for title in ch_titles:
    cited = sorted(find_citations(chapters.get(title, '')))
    print(f'  {title}: {cited} ({len(cited)} refs)')

# First occurrence
print('\n=== First Occurrence of Each Citation ===')
for n in range(1, 31):
    patterns = [
        f'textsuperscript{{[{n}]}}',
        f'textsuperscript{{[{n},',
        f', {n},',
        f', {n}]}}',
    ]
    min_line = None
    for p in patterns:
        idx = body.find(p)
        if idx >= 0:
            line = body[:idx].count('\n') + 1
            if min_line is None or line < min_line:
                min_line = line
    if min_line is not None:
        print(f'  [{n:2d}] first at line {min_line}')
    else:
        print(f'  [{n:2d}] *** UNCITED ***')

# Verify reference list
ref_items = re.findall(r'\\item\s*\[(\d+)\]', ref_section)
print(f'\nReference list has {len(ref_items)} items: {sorted(int(x) for x in ref_items)}')
if len(ref_items) != 30:
    print(f'*** WARNING: Expected 30 items, found {len(ref_items)} ***')
