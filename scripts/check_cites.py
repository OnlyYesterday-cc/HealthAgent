"""Map text citations to bibliography entries and find gaps."""
import re

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

body_end = content.find(r'\section*{参考文献}')
if body_end < 0:
    body_end = content.find(r'{参考文献}')
body = content[:body_end]
refs_section = content[body_end:]

# regex: \\textsuperscript{...}  -- need \\\\ for literal \ before t
# because \t is a TAB escape in Python regex
cite_pattern = re.compile(r'\\\\textsuperscript\{([^}]+)\}')
all_cited = set()
for m in cite_pattern.finditer(body):
    inner = m.group(1)
    for part in inner.split(','):
        part = part.strip()
        if '-' in part:
            a, b = part.split('-')
            for i in range(int(a), int(b)+1):
                all_cited.add(i)
        elif part.isdigit():
            all_cited.add(int(part))

# Parse reference items
ref_pattern = re.compile(r'\\item \[(\d+)\]')
all_refs = set()
for m in ref_pattern.finditer(refs_section):
    all_refs.add(int(m.group(1)))

print("=== References in list (sorted) ===")
print(sorted(all_refs))
print(f"Count: {len(all_refs)}")

print("\n=== Citations in body (sorted) ===")
print(sorted(all_cited))
print(f"Count: {len(all_cited)}")

print("\n=== In list but NOT cited in body ===")
uncited = sorted(all_refs - all_cited)
if uncited:
    for n in uncited:
        print(f"  [{n}]")
else:
    print("  None")

print("\n=== Cited in body but NOT in list ===")
missing = sorted(all_cited - all_refs)
if missing:
    for n in missing:
        print(f"  [{n}]")
else:
    print("  None")

print("\n=== Reference list numbering gaps (1 to max) ===")
max_ref = max(all_refs)
expected = set(range(1, max_ref + 1))
gaps = sorted(expected - all_refs)
if gaps:
    print(f"  Missing: {gaps}")
else:
    print(f"  Continuous 1-{max_ref}")
