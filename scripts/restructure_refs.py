"""
Restructure thesis references:
  - Ch1-Ch2: max 20 unique first appearances [1]-[20]
  - Ch3-Ch6: remaining first appearances [21]-[30]
  - >20 references must be post-2020

Steps:
  1. Renumber all \textsuperscript{[...]} markers in body
  2. Renumber & reorder \item [N] entries in bibliography
"""

THESIS = r'd:\HealthAgent\docs\thesis.tex'

# Old number -> New number mapping
OLD_TO_NEW = {
    1: 1, 2: 2,
    4: 3, 5: 4, 7: 5, 8: 6,
    9: 7, 11: 8, 12: 9, 13: 10, 10: 11,
    16: 12, 17: 13, 18: 14, 19: 15, 20: 16,
    21: 17, 22: 18, 23: 19, 24: 20,
    3: 21, 6: 22,
    14: 23,
    15: 24, 25: 25, 28: 26, 30: 27,
    26: 28, 27: 29, 29: 30,
}

# Verify
all_old = sorted(OLD_TO_NEW.keys())
assert all_old == list(range(1, 31)), f"Bad keys: {set(range(1,31)) - set(all_old)}"
all_new = sorted(OLD_TO_NEW.values())
assert all_new == list(range(1, 31)), f"Bad values: {set(range(1,31)) - set(all_new)}"
assert len(set(OLD_TO_NEW.values())) == 30, "Duplicate new numbers!"

with open(THESIS, 'r', encoding='utf-8') as f:
    content = f.read()

# Split at references section
for marker in [r'\section*{参考文献}', r'{参考文献}']:
    idx = content.find(marker)
    if idx >= 0:
        body = content[:idx]
        refs = content[idx:]
        break
else:
    raise RuntimeError("Cannot find references section")

def renumber_citation_inner(inner_text):
    """Renumber comma-separated citation numbers like '[21,10]' or '[4]'"""
    # Strip brackets
    text = inner_text.strip()
    has_brackets = text.startswith('[') and text.endswith(']')
    if has_brackets:
        text = text[1:-1]
    parts = []
    for part in text.split(','):
        part = part.strip()
        if '-' in part:
            a_str, b_str = part.split('-', 1)
            a = int(a_str.strip())
            b = int(b_str.strip())
            new_a = OLD_TO_NEW.get(a, a)
            new_b = OLD_TO_NEW.get(b, b)
            parts.append(f'{new_a}-{new_b}')
        elif part.lstrip('-').isdigit():
            # handle negative numbers too just in case
            n = int(part)
            parts.append(str(OLD_TO_NEW.get(n, n)))
        else:
            parts.append(part)
    result = ','.join(parts)
    if has_brackets:
        result = '[' + result + ']'
    return result

# Step 1: Renumber body citations
new_body_parts = []
pos = 0
prefix = r'\textsuperscript{'
while True:
    idx = body.find(prefix, pos)
    if idx < 0:
        new_body_parts.append(body[pos:])
        break
    new_body_parts.append(body[pos:idx])
    end = body.find('}', idx)
    if end < 0:
        new_body_parts.append(body[idx:])
        break
    inner = body[idx + len(prefix):end]
    new_inner = renumber_citation_inner(inner)
    new_body_parts.append(prefix + new_inner + '}')
    pos = end + 1
new_body = ''.join(new_body_parts)

# Step 2: Extract, renumber, and reorder bibliography items
ITEM_PREFIX = r'\item ['
ref_items = []  # list of (new_num, full_item_text)
pos = 0
while True:
    idx = refs.find(ITEM_PREFIX, pos)
    if idx < 0:
        break
    num_start = idx + len(ITEM_PREFIX)
    num_end = refs.find(']', num_start)
    if num_end < 0:
        break
    old_num = int(refs[num_start:num_end])

    # Find where this item ends
    next_item = refs.find(ITEM_PREFIX, idx + 1)
    end_env = refs.find(r'\end{enumerate}', idx)
    if next_item > 0:
        item_end = next_item
    else:
        item_end = end_env
    if item_end < 0:
        item_end = len(refs)

    item_text = refs[idx:item_end]
    new_num = OLD_TO_NEW.get(old_num, old_num)

    # Replace the number [old] -> [new] at the start of item
    old_tag = f'{ITEM_PREFIX}{old_num}]'
    new_tag = f'{ITEM_PREFIX}{new_num}]'
    new_item = item_text.replace(old_tag, new_tag, 1)

    ref_items.append((new_num, new_item))
    pos = item_end

# Sort by new number
ref_items.sort(key=lambda x: x[0])

# Reconstruct references section
enum_start = refs.find(r'\begin{enumerate}')
enum_end = refs.find(r'\end{enumerate}')
before_enum = refs[:enum_start + len(r'\begin{enumerate}')]
after_enum = refs[enum_end:]

new_refs = before_enum + '\n'
for _, item in ref_items:
    new_refs += item
new_refs += after_enum

# Step 3: Write
new_content = new_body + new_refs
with open(THESIS, 'w', encoding='utf-8') as f:
    f.write(new_content)

# Print summary
print("=== Renumbering complete ===")
for old, new in sorted(OLD_TO_NEW.items()):
    marker = " *" if old != new else ""
    print(f"  [{old}] -> [{new}]{marker}")

# Count post-2020
pre2020_new = {2, 8, 21, 22, 24}
post2020 = 30 - len(pre2020_new)
print(f"\nPost-2020: {post2020}/30")
print(f"Pre-2020: {sorted(pre2020_new)}")

# Verify: count citations in body
cite_count = 0
pos = 0
while True:
    idx = new_body.find(r'\textsuperscript{', pos)
    if idx < 0:
        break
    cite_count += 1
    pos = idx + 1
print(f"Body citations: {cite_count}")
