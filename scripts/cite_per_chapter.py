#!/usr/bin/env python3
"""Count citations per actual chapter."""
import re

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

ref_start = content.find(r'\section*{参考文献}')
body = content[:ref_start]

sections = list(re.finditer(r'\\section\{([^}]+)\}', body))
for i, m in enumerate(sections):
    title = m.group(1)
    start = m.start()
    end = sections[i+1].start() if i+1 < len(sections) else len(body)
    ch_body = body[start:end]
    nums = set()
    for mm in re.finditer(r'textsuperscript\{\[([0-9,\s]+)\]\}', ch_body):
        for n in mm.group(1).split(','):
            nums.add(int(n.strip()))
    cited = sorted(nums)
    print(f'{title}: {cited} ({len(cited)}篇)')
