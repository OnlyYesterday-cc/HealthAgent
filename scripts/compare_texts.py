"""Compare thesis PDF text vs DOCX reference - output to file to avoid encoding issues."""
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'd:\HealthAgent\docs\_pdf_text.txt', 'r', encoding='utf-8') as f:
    pdf_raw = f.read()
with open(r'd:\HealthAgent\docs\_docx_text.txt', 'r', encoding='utf-8') as f:
    docx_raw = f.read()

# Remove PDF artifacts
pdf = pdf_raw
pdf = re.sub(r'=== PAGE \d+ ===\n?', '', pdf)
pdf = re.sub(r'华中科技大学本科毕业设计（论文）\n', '', pdf)
pdf = re.sub(r'^\d+\n', '', pdf, flags=re.MULTILINE)

def normalize(text):
    text = text.replace('\n', '')
    text = re.sub(r'\s+', '', text)
    return text.strip()

pdf_norm = normalize(pdf)
docx_norm = normalize(docx_raw)

# Write results to file
out_path = r'd:\HealthAgent\docs\_comparison_result.txt'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(f"PDF normalized length: {len(pdf_norm)}\n")
    f.write(f"DOCX normalized length: {len(docx_norm)}\n\n")

    # Check key sections
    f.write("=== Major section location check ===\n")
    markers = ['摘要', 'Abstract', '目', '绪论', '研究背景与意义', '相关技术',
               '需求分析与健康管理智能体设计', '功能需求', '非功能需求',
               '健康管理智能体工具模块实现', '双通路OCR血压计图像识别',
               '健康管理智能体测评', '结论与展望', '参考文献', '附', '致谢']
    for marker in markers:
        pdf_pos = pdf_norm.find(marker)
        docx_pos = docx_norm.find(marker)
        ctx = 30
        if pdf_pos >= 0 and docx_pos >= 0:
            pdf_ctx = pdf_norm[max(0,pdf_pos-ctx):pdf_pos+len(marker)+ctx]
            docx_ctx = docx_norm[max(0,docx_pos-ctx):docx_pos+len(marker)+ctx]
            if pdf_ctx == docx_ctx:
                f.write(f"  [OK] '{marker}' - context matches\n")
            else:
                f.write(f"  [DIFF] '{marker}' - context differs!\n")
                f.write(f"    PDF:  ...{repr(pdf_ctx[:100])}...\n")
                f.write(f"    DOCX: ...{repr(docx_ctx[:100])}...\n")
        elif pdf_pos < 0:
            f.write(f"  [MISSING] '{marker}' - NOT in PDF!\n")
        else:
            f.write(f"  [MISSING] '{marker}' - NOT in DOCX!\n")

    # Overall similarity
    import difflib
    matcher = difflib.SequenceMatcher(None, pdf_norm, docx_norm)
    ratio = matcher.ratio()
    f.write(f"\nNormalized text similarity: {ratio:.6f}\n")

    # Show real differences
    if ratio < 1.0:
        f.write("\n=== Real text differences (non-whitespace) ===\n")
        seen = set()
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != 'equal':
                pdf_s = pdf_norm[i1:i2]
                docx_s = docx_norm[j1:j2]
                if pdf_s or docx_s:
                    key = (pdf_s[:60], docx_s[:60])
                    if key not in seen:
                        seen.add(key)
                        if len(seen) <= 50:
                            f.write(f"  [{len(seen)}] {tag}:\n")
                            f.write(f"    PDF:  {repr(pdf_s[:120])}\n")
                            f.write(f"    DOCX: {repr(docx_s[:120])}\n")
        f.write(f"\nTotal unique text differences: {len(seen)}\n")

        if len(seen) == 0:
            f.write("Text content is IDENTICAL after whitespace normalization.\n")

print(f"Comparison complete. Results written to {out_path}")
print(f"Normalized similarity: {ratio:.6f}")
print(f"Unique text diffs: {len(seen) if ratio < 1.0 else 0}")
