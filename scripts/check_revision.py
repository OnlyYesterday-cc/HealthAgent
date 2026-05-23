#!/usr/bin/env python3
"""Check thesis against all 17 revision points."""
import re

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

issues = []
ref_start = content.find(r'\section*{参考文献}')
body = content[:ref_start] if ref_start > 0 else content

# === 1. 摘要检查 ===
cn_abs_start = content.find(r'\section*{摘')
cn_abs_end = content.find(r'\section*{Abstract}', cn_abs_start)
cn_abs = content[cn_abs_start:cn_abs_end] if cn_abs_end > 0 else ''

benwei = cn_abs.count('本文')
if benwei > 0:
    issues.append(f'1. 摘要出现"本文" {benwei} 次，应避免以"本文"为主语')

# === 2. 英文缩写全称 ===
abbrs = [
    ('OCR', 'Optical Character Recognition'),
    ('RAG', 'Retrieval-Augmented Generation'),
    ('VLM', 'Vision-Language Model'),
    ('LLM', 'Large Language Model'),
    ('HOG', 'Histogram of Oriented Gradients'),
    ('SVM', 'Support Vector Machine'),
    ('SSE', 'Server-Sent Events'),
    ('JWT', 'JSON Web Token'),
    ('ORM', 'Object-Relational Mapping'),
    ('CLAHE', 'Contrast Limited Adaptive Histogram Equalization'),
    ('CTC', 'Connectionist Temporal Classification'),
    ('CRNN', 'Convolutional Recurrent Neural Network'),
    ('SMA', 'Simple Moving Average'),
    ('LSTM', 'Long Short-Term Memory'),
    ('ARIMA', 'Autoregressive Integrated Moving Average'),
    ('BERT', 'Bidirectional Encoder Representations from Transformers'),
]
for abbr, full in abbrs:
    idx = content.find(abbr)
    if idx > 0:
        before = content[max(0, idx-200):idx]
        if full not in before:
            issues.append(f'2. {abbr} 首次出现前200字符内未找到全称 "{full}"')

# === 5. 第三章二级标题下段落数 ===
ch3_start = content.find(r'\section{健康管理智能体需求分析与设计}')
ch4_start = content.find(r'\section{健康管理智能体工具模块实现}')
ch3_body = content[ch3_start:ch4_start]

# Find all subsections
subs = list(re.finditer(r'\\subsection\{([^}]+)\}', ch3_body))
for i, m in enumerate(subs):
    title = m.group(1)
    sec_start = m.end()
    sec_end = subs[i+1].start() if i+1 < len(subs) else len(ch3_body)
    sec_content = ch3_body[sec_start:sec_end]
    # Count paragraphs (separated by blank lines, excluding headings)
    paragraphs = [p for p in sec_content.split('\n\n') if p.strip()
                  and not p.strip().startswith('\\') and not p.strip().startswith('%')]
    if len(paragraphs) < 3 and title not in ['本章小结', '功能需求']:
        issues.append(f'5. Ch3小节"{title}"仅{len(paragraphs)}段，建议≥3段')

# === 6. 4.1.2节标题 ===
if r'\subsubsection{OCR方案对比分析}' not in content:
    issues.append('6. 4.1.2节标题应为"OCR方案对比分析"')

# === 8. 1.2节引用 ===
sec12_start = content.find(r'\subsection{国内外研究现状}')
if sec12_start > 0:
    rest = content[sec12_start+50:]
    next_sub = rest.find(r'\subsection{')
    sec12_body = rest[:next_sub] if next_sub > 0 else rest[:20000]
    refs = set()
    for m in re.finditer(r'textsuperscript\{\[([0-9,\s]+)\]\}', sec12_body):
        for n in m.group(1).split(','):
            refs.add(int(n.strip()))
    print(f'[INFO] 1.2节: {len(refs)}篇, {sorted(refs)}')
    if len(refs) < 10:
        issues.append(f'8. 1.2节仅引用{len(refs)}篇，应有10-20篇')

# === 9. 口语化 ===
colloquial_words = [
    '干嘛', '说白了', '搞定', '不咋', '为啥', '挺多', '啥', '咋',
    '吧。', '嘛。', '呀。', '啦。', '呢。', '有点', '没法',
    '不干净', '接着做', '说一下',
]
for word in colloquial_words:
    count = content.count(word)
    if count > 0:
        idx = content.find(word)
        ctx = content[max(0,idx-15):idx+len(word)+15].replace('\n',' ')
        issues.append(f'9. 口语化词"{word}"出现{count}次，如:...{ctx}...')

# Also check sentence-ending particles followed by period
for particle in ['吧', '嘛', '呀', '啦', '呢']:
    count = content.count(particle + '。')
    if count > 0:
        idx = content.find(particle + '。')
        ctx = content[max(0,idx-15):idx+20].replace('\n',' ')
        issues.append(f'9. 口语化句尾"{particle}。"出现{count}次，如:...{ctx}...')

# === 10. 本章小结 ===
for ch_num, sec_title in [(2, '相关技术'), (3, '健康管理智能体需求分析与设计'),
                            (4, '健康管理智能体工具模块实现'), (5, '健康管理智能体测评')]:
    pattern = rf'\\section{{{sec_title}}}'
    m = re.search(pattern, content)
    if m:
        ch_start = m.start()
        # Find next section
        rest = content[ch_start+50:]
        next_sec = rest.find(r'\section{')
        ch_body = rest[:next_sec] if next_sec > 0 else rest
        if r'\subsection{本章小结}' not in ch_body:
            issues.append(f'10. 第{ch_num}章缺少"本章小结"')

# === 14. 图表引用 ===
labels = re.findall(r'\\label\{([^}]+)\}', content)
for label in labels:
    if label.startswith('fig:') or label.startswith('tab:'):
        ref_count = body.count(rf'\ref{{{label}}}')
        if ref_count == 0:
            issues.append(f'14. 标签 {label} 未在正文中引用')

# === 15. 结论格式 ===
concl_start = content.find(r'\subsection{工作总结}')
concl_end = content.find(r'\subsection{存在的不足}', concl_start)
conclusion = content[concl_start:concl_end] if concl_end > 0 else ''
# Should have 3 numbered points
if '（1）' not in conclusion or '（2）' not in conclusion or '（3）' not in conclusion:
    issues.append('15. 结论应列3点，格式为（1）（2）（3）')

# === 16. 参考文献总条数 ===
ref_items = len(re.findall(r'\\item\s', content[ref_start:ref_start+5000]))
print(f'[INFO] 参考文献约 {ref_items} 条')

# === Print results ===
print('\n=== 还需处理的问题 ===')
if issues:
    for i, iss in enumerate(issues, 1):
        print(f'  {i}. {iss}')
else:
    print('  未发现问题')
print(f'\n共 {len(issues)} 项待处理')
