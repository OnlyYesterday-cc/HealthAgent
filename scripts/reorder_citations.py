#!/usr/bin/env python3
"""
Reorder references to match first-citation order.
Renumbers all \\textsuperscript{[N]} in body and reorders the reference list.
"""
import re

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

# Split body and reference section
ref_section_start = content.find(r'\section*{参考文献}')
body = content[:ref_section_start]
ref_section = content[ref_section_start:]

# Find first citation position for each reference number
first_pos = {}
for n in range(1, 31):
    min_pos = float('inf')
    patterns = [
        f'textsuperscript{{[{n}]}}',
        f'textsuperscript{{[{n},',
        f', {n},',
        f', {n}]}}',
    ]
    for p in patterns:
        pos = body.find(p)
        if pos >= 0 and pos < min_pos:
            min_pos = pos
    if min_pos < float('inf'):
        first_pos[n] = min_pos

# Sort by first appearance = new numbering
sorted_nums = sorted(first_pos.items(), key=lambda x: x[1])
old_to_new = {}
for new_num, (old_num, pos) in enumerate(sorted_nums, 1):
    old_to_new[old_num] = new_num

print('Citations renumbered:')
changes = 0
for old, new in sorted(old_to_new.items()):
    if old != new:
        print(f'  [{old}] -> [{new}]')
        changes += 1
print(f'Total changes: {changes} references renumbered')

if changes == 0:
    print('No renumbering needed!')
    exit(0)

# Renumber citations in body text
# Process from highest old number to lowest to avoid conflicts
def replace_citation(match):
    nums_str = match.group(1)
    nums = [n.strip() for n in nums_str.split(',')]
    new_nums = [str(old_to_new[int(n)]) for n in nums]
    new_nums.sort(key=int)
    return '\\textsuperscript{[' + ','.join(new_nums) + ']}'

body_new = re.sub(r'\\textsuperscript\{\[([0-9,\s]+)\]\}', replace_citation, body)

# Reorder reference list items
items_marker = r'\begin{enumerate}[label={[\arabic*]}]'
items_start = ref_section.find(items_marker)
items_end = ref_section.find(r'\end{enumerate}', items_start)
end_marker_len = len(r'\end{enumerate}')

preamble = ref_section[:items_start + len(items_marker)]
items_content = ref_section[items_start + len(items_marker):items_end]
postamble = ref_section[items_end:]

# Split into individual items
item_blocks = items_content.split(r'\item')
item_blocks = [b.strip() for b in item_blocks if b.strip()]

# new_to_old: position N in new list = which old item goes there
new_to_old = {v: k for k, v in old_to_new.items()}

reordered = []
for n in range(1, 31):
    old_n = new_to_old.get(n, n)
    if old_n <= len(item_blocks):
        reordered.append(item_blocks[old_n - 1])

# Rebuild
new_items = '\n    \\item ' + '\n\n    \\item '.join(reordered)
new_ref_block = preamble + '\n' + new_items + '\n\n' + r'\end{enumerate}'
ref_section_new = ref_section[:items_start] + new_ref_block + ref_section[items_end + end_marker_len:]

# Reassemble and save
content = body_new + ref_section_new

with open(r'd:\HealthAgent\docs\thesis.tex', 'w', encoding='utf-8') as f:
    f.write(content)

# Final verification
ref_check = content.find(r'\section*{参考文献}')
body_check = content[:ref_check]
cited_check = {}
for m in re.finditer(r'textsuperscript\{\[(\d+)\]', body_check):
    n = int(m.group(1))
    cited_check[n] = cited_check.get(n, 0) + 1
for m in re.finditer(r'textsuperscript\{\[(\d+),(\d+)\]', body_check):
    a, b = int(m.group(1)), int(m.group(2))
    cited_check[a] = cited_check.get(a, 0) + 1
    cited_check[b] = cited_check.get(b, 0) + 1

uncited = sorted(set(range(1,31)) - set(cited_check.keys()))
if uncited:
    print(f'\nWARNING - uncited: {uncited}')
else:
    print(f'\nAll 30 references cited after renumbering')
print(f'Total citations: {sum(cited_check.values())}')

# Show new order by first appearance
first_new = {}
for n in range(1, 31):
    pos = body_check.find(f'textsuperscript{{[{n}]}}')
    if pos < 0:
        pos = body_check.find(f'textsuperscript{{[{n},')
    if pos < 0:
        pos = body_check.find(f', {n},')
    if pos < 0:
        pos = body_check.find(f', {n}]}}')
    if pos >= 0:
        first_new[n] = pos

sorted_new = sorted(first_new.items(), key=lambda x: x[1])
print('\nNew order (by first citation):')
for rank, (num, pos) in enumerate(sorted_new, 1):
    line = body_check[:pos].count('\n') + 1
    mark = ' <--' if rank != num else ''
    print(f'  [{num}] first at order {rank} (line {line}){mark}')
