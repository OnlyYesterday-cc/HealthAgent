"""
Fix citation-bibliography mapping in thesis.tex.

1. Map each text citation to correct bibliography entry
2. Replace both with key-based references
3. Remove low-quality/duplicative references
4. Output ready for renumbering script
"""

import re
import sys

THESIS = "d:/HealthAgent/docs/thesis.tex"

# Mapping from CURRENT text citation number to bib key (r01-r36)
# Determined by manual trace of citation context → bibliography entry
CITE_TO_KEY = {
    '1':  'r01',  # 中国心血管健康与疾病报告2023
    '2':  'r02',  # 中国高血压防治指南2018
    '3':  'r03',  # Tesseract
    '4':  'r04',  # PP-OCR / PaddleOCR
    '5':  'r28',  # PaddleOCR 3.0 2025
    '6':  'r05',  # HOG 2005
    '7':  'r16',  # Soeno 2024
    '8':  'r17',  # Ferreira 2025
    '9':  'r18',  # Neveditsin 2025
    '10': 'r19',  # Chau 2025
    '11': 'r33',  # Raquib 2025 Cureus
    '12': 'r34',  # Lindsay-Perez 2025
    '13': 'r31',  # 刘畅 2026
    '14': 'r07',  # Alessa 2019
    '15': 'r20',  # 张悦 2024
    '16': 'r21',  # Abe 2025
    '17': 'r22',  # Gupta 2025 TFT
    '18': 'r08',  # BERT 2019
    '19': 'r09',  # Singhal Nature 2023
    '20': 'r10',  # Med-PaLM 2 2023
    '21': 'r11',  # 刘知远 2023
    '22': 'r12',  # 李飞飞 2024
    '23': 'r13',  # Stanford HAI 2024
    '24': 'r30',  # Santulli 2026
    '25': 'r32',  # Smith 2025 MDPI
    '26': 'r14',  # 高血压指南2024
    '27': 'r29',  # ESC 2024
    '28': 'r15',  # Lewis RAG 2020
    '29': 'r23',  # 王浩 2025 JAMIA
    '30': 'r24',  # Lee 2025 PLOS DH
    '31': 'r25',  # He 2025 arXiv
    '32': 'r26',  # Chen 2025 CARES
    '33': 'r27',  # Williams 2025 NPJ DM
    '34': 'r35',  # Patel 2025 NeurIPS
    '35': 'r36',  # Thompson 2025
}

# Keys to DELETE (low quality / duplicative)
DELETE_KEYS = {'r13', 'r18', 'r19', 'r25', 'r33', 'r36'}  # 6 cuts → 30 remaining

# Keys to keep but need their text citation fixed
# r06 (GPT-4) has NO text citation - need to add one!
MISSING_CITATIONS = {
    'r06': True,  # GPT-4 is not cited in text
}

with open(THESIS, "r", encoding="utf-8") as f:
    content = f.read()

# Split into body and bibliography
bib_start = content.find(r'\begin{enumerate}[label={[\arabic*]}]')
bib_end = content.find(r'\end{enumerate}', bib_start) + len(r'\end{enumerate}')
body = content[:bib_start]
bib_section = content[bib_start:bib_end]
after_bib = content[bib_end:]

# Parse bib items
bib_parts = bib_section.split(r'\item ')
bib_preamble = bib_parts[0]  # \begin{enumerate}...
bib_items_raw = bib_parts[1:]  # each item's content

print(f"Found {len(bib_items_raw)} bib items")

# Replace text citations
def replace_text_cite(match):
    nums = [n.strip() for n in match.group(1).split(',') if n.strip().isdigit()]
    new_nums = []
    for n in nums:
        if n in CITE_TO_KEY:
            key = CITE_TO_KEY[n]
            if key not in DELETE_KEYS:
                new_nums.append(key)
            # If key is deleted, skip it (remove from citation)
        else:
            print(f"WARNING: No mapping for citation [{n}]")
            new_nums.append(f"UNMAPPED_{n}")
    if not new_nums:
        return ''  # Remove empty citation
    return '\\textsuperscript{[' + ','.join(new_nums) + ']}'

cite_pattern = re.compile(r'\\textsuperscript\{\[([^\]]+)\]\}')
body = cite_pattern.sub(replace_text_cite, body)

# Rebuild bibliography
new_bib_items = []
for i, item in enumerate(bib_items_raw):
    key = f"r{i+1:02d}"
    if key in DELETE_KEYS:
        print(f"  Deleting [{key}]")
        continue
    new_bib_items.append(f'\\item [{key}]' + item)

# Keep enumerate but remove label=... since we use explicit keys
new_bib = '\\begin{enumerate}\n' + '\n'.join(new_bib_items) + '\n\\end{enumerate}'

# Reassemble
new_content = body + '\n' + new_bib + after_bib

with open(THESIS, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"\nKept {len(new_bib_items)} references")
print("Done. Now run renumber_refs.py to get sequential numbers.")
