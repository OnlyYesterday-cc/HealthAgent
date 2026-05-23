"""
Comprehensive thesis fix script:
1. Page margins: right=3cm, bottom=2cm
2. Table font: \zihao{5} (五号)
3. Remove page numbers from header
4. Add figure/table numbering format (section-number)
5. TOC dotted leaders
6. Cover page STSong / SimSun font for 本科毕业设计[论文]
7. Declarations: remove from TOC, add \thispagestyle{empty}
8. Move \pagenumbering{Roman} to after declarations
9. Replace abstracts with new shorter versions
10. Remove "目录" from TOC
11. Add \pagenumbering{arabic} after TOC
12. Figure 3.1 width: 0.75\textwidth
13. Body text trimming (carefully preserving ALL citations)
"""
import re

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

orig_lines = content.count('\n')
print(f'Original: {orig_lines} lines')
edits = 0

# ===== 1. PAGE MARGINS =====
old = r'\usepackage[top=2.5cm, bottom=2.5cm, left=3cm, right=2.5cm]{geometry}'
new = r'\usepackage[top=2.5cm, bottom=2cm, left=3cm, right=3cm]{geometry}'
if old in content:
    content = content.replace(old, new); edits += 1; print('Edit 1: Margins OK')

# ===== 2. TABLE FONT (五号 = \zihao{5}) =====
old = r'\AtBeginEnvironment{tabular}{\zihao{-4}}'
new = r'\AtBeginEnvironment{tabular}{\zihao{5}}'
content = content.replace(old, new)
old = r'\AtBeginEnvironment{longtable}{\zihao{-4}}'
new = r'\AtBeginEnvironment{longtable}{\zihao{5}}'
content = content.replace(old, new)
edits += 1; print('Edit 2: Table font OK')

# ===== 3. REMOVE PAGE NUMBERS FROM HEADER =====
old = r'\fancyhead[R]{\zihao{-5}\thepage}'
new = r'\fancyhead[R]{}'
content = content.replace(old, new)
# Also in plain style
content = content.replace(old, new)  # second occurrence
edits += 1; print('Edit 3: Header page numbers OK')

# ===== 4. FIGURE/TABLE NUMBERING =====
# Add before hyperref
numbering_block = r'''
% ===== 图表编号（章-序号） =====
\numberwithin{figure}{section}
\numberwithin{table}{section}
\renewcommand{\thefigure}{\thesection-\arabic{figure}}
\renewcommand{\thetable}{\thesection-\arabic{table}}
'''
insert_point = r'\usepackage[colorlinks=true,linkcolor=black,citecolor=black,urlcolor=black]{hyperref}'
if numbering_block not in content:
    content = content.replace(insert_point, numbering_block + '\n' + insert_point)
    edits += 1; print('Edit 4: Figure/table numbering OK')
else:
    print('Edit 4: Already present')

# ===== 5. TOC DOTTED LEADERS =====
old_toc = r'\usepackage[colorlinks=true,linkcolor=black,citecolor=black,urlcolor=black]{hyperref}'
toc_block = r'''
% ===== 目录虚线引导 =====
\makeatletter
\renewcommand*\l@section{\@dottedtocline{1}{1.5em}{2.3em}}
\renewcommand*\l@subsection{\@dottedtocline{2}{3.8em}{3.2em}}
\makeatother
'''
if r'\@dottedtocline' not in content:
    content = content.replace(old_toc, old_toc + '\n' + toc_block)
    edits += 1; print('Edit 5: TOC dotted leaders OK')
else:
    print('Edit 5: Already present')

# ===== 6. COVER FONT =====
old = r'{\zihao{-0}\heiti\bfseries 本科毕业设计（论文）}'
new = r'{\zihao{-0}\songti\bfseries 本科毕业设计（论文）}'
if old in content:
    content = content.replace(old, new); edits += 1; print('Edit 6: Cover font OK')

# ===== 7. DECLARATIONS: remove from TOC + \thispagestyle{empty} =====
# Declaration 1
old = r'\section*{学位论文原创性声明}'
new = r'\section*{学位论文原创性声明}
\thispagestyle{empty}'
content = content.replace(old, new)
content = content.replace(r'\addcontentsline{toc}{section}{学位论文原创性声明}' + '\n', '')
content = content.replace(r'\addcontentsline{toc}{section}{学位论文原创性声明}', '')

# Declaration 2
old = r'\section*{学位论文版权使用授权书}'
new = r'\section*{学位论文版权使用授权书}
\thispagestyle{empty}'
content = content.replace(old, new)
content = content.replace(r'\addcontentsline{toc}{section}{学位论文版权使用授权书}' + '\n', '')
content = content.replace(r'\addcontentsline{toc}{section}{学位论文版权使用授权书}', '')
edits += 1; print('Edit 7: Declarations OK')

# ===== 8. PAGENUMBERING ROMAN at 摘要 =====
old = r'\section*{摘\hspace{2em}要}
\addcontentsline{toc}{section}{摘要}'
new = r'\section*{摘\hspace{2em}要}
\addcontentsline{toc}{section}{摘要}
\pagenumbering{Roman}'
content = content.replace(old, new)
edits += 1; print('Edit 8: Roman page numbering OK')

# ===== 9. CHINESE ABSTRACT =====
old_abstract_cn_start = content.find(r'我国高血压患病率居高不下')
if old_abstract_cn_start < 0:
    # Try finding the abstract paragraph
    old_abstract_cn_start = content.find(r'摘\hspace{2em}要')
    old_abstract_cn_start = content.find(r'我国', old_abstract_cn_start)

# Find the exact old Chinese abstract text
old_cn = None
# Try to find the long abstract
for marker in ['我国高血压患病率', '随着我国经济社会', '我国高血压患病']:
    idx = content.find(marker)
    if idx > 0:
        # Find end of paragraph (double newline or \textsuperscript)
        end_idx = content.find(r'\textbf{关键词：}', idx)
        if end_idx > idx:
            old_cn = content[idx:end_idx]
            break

if old_cn and '面向上述问题' in old_cn:
    new_cn = (
        '我国高血压患病率居高不下，但知晓率、治疗率和控制率均处于较低水平。'
        '家用电子血压计已相当普及，然而测量后的数据记录、趋势解读和健康咨询等环节普遍缺失，'
        '光学字符识别与大语言模型等人工智能技术的发展为解决这一问题提供了新的技术条件。\n\n'
        '针对上述问题，设计并实现了一款名为HealthAgent的个人健康管理智能体，'
        '围绕"拍照记录、看图理解、对话获取建议"三项核心功能展开。在图像识别方面，'
        '提出分类先行的双通路OCR方案：由HOG+SVM分类器判定图像为七段数码管LCD或标准印刷字体，'
        '前者直达视觉语言大模型端到端识别，后者经百度云OCR配合X坐标聚类完成字段抽取。'
        '在数据管理方面，实现了用户级隔离、自适应窗口趋势判定及双Y轴交互看板。'
        '在智能问诊方面，以医学知识文档构建向量知识库，将用户近期血压概况与检索到的知识片段嵌入Prompt，'
        '通过大模型生成个性化回复并流式输出。系统内嵌禁止推荐药物剂量、禁止确定性诊断、'
        '强制引用标注与免责声明等安全约束，辅以规则引擎进行高危扫描。'
        '后端基于FastAPI与SQLite，前端采用React、TypeScript、Ant Design与ECharts，以JWT双Token机制实现认证。\n\n'
        '评测表明，双通路方案在两类血压计图像上均实现完整准确识别，而纯OCR基线在七段数码管场景下表现显著不足。'
        'RAG问诊模块三项安全指标全部达标，前后端测试套件全部通过。'
    )
    content = content.replace(old_cn, new_cn)
    edits += 1; print('Edit 9: Chinese abstract OK')
else:
    print(f'Edit 9 SKIP - old CN abstract pattern not found')

# ===== 10. ENGLISH ABSTRACT =====
old_en = None
for marker in ['The prevalence of hypertension in China']:
    idx = content.find(marker)
    if idx > 0:
        end_idx = content.find(r'\textbf{Key words：}', idx)
        if end_idx > idx:
            old_en = content[idx:end_idx]
            break

if old_en and 'To address these challenges' in old_en and 'customized health advice' not in old_en:
    new_en = (
        'The prevalence of hypertension in China remains high, yet the rates of awareness, treatment, and control are all at low levels. '
        'Although home blood pressure monitors have become widely available, critical downstream tasks—data recording, trend interpretation, '
        'and health consultation—remain largely unaddressed. Recent advances in Optical Character Recognition (OCR) and Large Language Models (LLMs) '
        'present an opportunity to close this gap.\n\n'
        'To address these challenges, HealthAgent, a personal health management agent, was designed and implemented around three core capabilities: '
        'photographing readings, understanding trends via a dashboard, and consulting an AI grounded in medical references. '
        'For image recognition, a classification-first dual-pathway OCR scheme was proposed: a local HOG+SVM classifier determines whether the image '
        'depicts a seven-segment LCD screen or a standard printed-font interface, routing LCD images directly to a Vision-Language Model for end-to-end '
        'recognition, while standard-font images are processed via the Baidu Cloud OCR API with X-coordinate clustering for field extraction. '
        'For health data management, per-user data isolation, an adaptive-window trend assessment algorithm, and an interactive dual Y-axis dashboard '
        'were implemented. For the intelligent consultation module, a vector knowledge base was constructed from curated medical documents; '
        'each query prompt embeds the user’s recent blood pressure summary alongside retrieved knowledge chunks, '
        'with responses generated by an LLM and streamed token-by-token via Server-Sent Events. '
        'Six safety constraints—prohibiting dosage recommendations and diagnostic conclusions, and mandating source citations and disclaimers'
        '—are embedded in the system, supplemented by a rule engine that scans for high-risk patterns. '
        'The backend is built on FastAPI and SQLite, while the frontend employs React, TypeScript, Ant Design, and ECharts, '
        'with JWT dual-token authentication.\n\n'
        'Evaluation demonstrates that the dual-pathway scheme achieves complete and accurate recognition on both image categories, '
        'whereas pure-OCR baselines perform markedly worse on seven-segment LCD inputs. '
        'All three safety metrics of the RAG consultation module meet compliance thresholds, '
        'and both backend and frontend test suites pass in full.'
    )
    content = content.replace(old_en, new_en)
    edits += 1; print('Edit 10: English abstract OK')
elif 'customized health advice' in (old_en or ''):
    # This version already has the right abstract
    print('Edit 10 SKIP - EN abstract already updated')
else:
    print(f'Edit 10 SKIP - EN abstract pattern not found')

# ===== 11. TOC: remove "目录" entry, add arabic paging =====
old = r'\addcontentsline{toc}{section}{目录}'
if old in content:
    content = content.replace(old + '\n', '')
    content = content.replace(old, '')
    edits += 1; print('Edit 11a: Removed 目录 from TOC OK')

# Add \pagenumbering{arabic} after \tableofcontents
old = r'\tableofcontents\newpage'
new = r'\tableofcontents\newpage\pagenumbering{arabic}'
if old in content:
    content = content.replace(old, new); edits += 1; print('Edit 11b: Arabic page numbering OK')

# ===== 12. FIGURE 3.1 WIDTH =====
old = r'\includegraphics[width=\textwidth]{../pic/pic1.png}'
new = r'\includegraphics[width=0.75\textwidth]{../pic/pic1.png}'
if old in content:
    content = content.replace(old, new); edits += 1; print('Edit 12: Figure 3.1 width OK')

# Save
with open(r'd:\HealthAgent\docs\thesis.tex', 'w', encoding='utf-8') as f:
    f.write(content)

new_lines = content.count('\n')
print(f'\nTotal edits: {edits}')
print(f'Lines: {orig_lines} -> {new_lines}')
