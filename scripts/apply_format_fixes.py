#!/usr/bin/env python3
"""Apply all formatting fixes to thesis.tex"""
import sys

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content.count('\n')
print(f'Original: {orig} lines')
fixes = 0

# 1. Page margins
old = r'\usepackage[top=2.5cm, bottom=2.5cm, left=3cm, right=2.5cm]{geometry}'
new = r'\usepackage[top=2.5cm, bottom=2cm, left=3cm, right=3cm]{geometry}'
content = content.replace(old, new)
fixes += 1
print('1. Margins OK')

# 2. Table font
content = content.replace(r'\AtBeginEnvironment{tabular}{\zihao{-4}}', r'\AtBeginEnvironment{tabular}{\zihao{5}}')
content = content.replace(r'\AtBeginEnvironment{longtable}{\zihao{-4}}', r'\AtBeginEnvironment{longtable}{\zihao{5}}')
fixes += 1
print('2. Table font OK')

# 3. Remove page numbers from header (both fancy and plain)
old_header = r'\fancyhead[R]{\zihao{-5}\thepage}'
new_header = r'\fancyhead[R]{}'
content = content.replace(old_header, new_header)
fixes += 1
print('3. Header page numbers removed OK')

# 4. Figure/table numbering
numbering_block = (
    r'\numberwithin{figure}{section}' + '\n'
    r'\numberwithin{table}{section}' + '\n'
    r'\renewcommand{\thefigure}{\thesection-\arabic{figure}}' + '\n'
    r'\renewcommand{\thetable}{\thesection-\arabic{table}}' + '\n'
)
if r'\numberwithin{figure}{section}' not in content:
    marker = r'\usepackage[colorlinks=true,linkcolor=black,citecolor=black,urlcolor=black]{hyperref}'
    content = content.replace(marker, numbering_block + marker)
    fixes += 1
    print('4. Figure/table numbering added OK')
else:
    print('4. Numbering already present')

# 5. TOC dotted leaders
toc_dots = (
    r'\makeatletter' + '\n'
    r'\renewcommand*\l@section{\@dottedtocline{1}{1.5em}{2.3em}}' + '\n'
    r'\renewcommand*\l@subsection{\@dottedtocline{2}{3.8em}{3.2em}}' + '\n'
    r'\makeatother' + '\n'
)
if r'\@dottedtocline' not in content:
    marker = r'\usepackage[colorlinks=true,linkcolor=black,citecolor=black,urlcolor=black]{hyperref}'
    content = content.replace(marker, marker + '\n' + toc_dots)
    fixes += 1
    print('5. TOC dotted leaders added OK')
else:
    print('5. Already present')

# 6. Cover font
old = r'{\zihao{-0}\heiti\bfseries 本科毕业设计（论文）}'
new = r'{\zihao{-0}\songti\bfseries 本科毕业设计（论文）}'
content = content.replace(old, new)
fixes += 1
print('6. Cover font OK')

# 7-8. Declarations: add \thispagestyle{empty}, remove from TOC
# Declaration 1
old1 = r'\section*{学位论文原创性声明}'
new1 = r'\section*{学位论文原创性声明}' + '\n' + r'\thispagestyle{empty}'
content = content.replace(old1, new1)
content = content.replace(r'\addcontentsline{toc}{section}{学位论文原创性声明}' + '\n', '')
content = content.replace(r'\addcontentsline{toc}{section}{学位论文原创性声明}', '')

# Declaration 2
old2 = r'\section*{学位论文版权使用授权书}'
new2 = r'\section*{学位论文版权使用授权书}' + '\n' + r'\thispagestyle{empty}'
content = content.replace(old2, new2)
content = content.replace(r'\addcontentsline{toc}{section}{学位论文版权使用授权书}' + '\n', '')
content = content.replace(r'\addcontentsline{toc}{section}{学位论文版权使用授权书}', '')
fixes += 1
print('7. Declarations OK')

# 9. Page numbering: Roman at Chinese abstract
old = r'\section*{摘\hspace{2em}要}' + '\n' + r'\addcontentsline{toc}{section}{摘要}'
new = r'\section*{摘\hspace{2em}要}' + '\n' + r'\addcontentsline{toc}{section}{摘要}' + '\n' + r'\pagenumbering{Roman}'
content = content.replace(old, new)
fixes += 1
print('8. Roman page numbering OK')

# 10. Remove "目录" from TOC
content = content.replace(r'\addcontentsline{toc}{section}{目录}' + '\n', '')
content = content.replace(r'\addcontentsline{toc}{section}{目录}', '')
fixes += 1
print('9. TOC 目录 removed OK')

# 11. Arabic page numbering after TOC
old = r'\tableofcontents\newpage'
new = r'\tableofcontents\newpage' + '\n' + r'\pagenumbering{arabic}'
content = content.replace(old, new)
fixes += 1
print('10. Arabic page numbering OK')

# 12. Figure 3.1 width
old = r'\includegraphics[width=\textwidth]{../pic/pic1.png}'
new = r'\includegraphics[width=0.75\textwidth]{../pic/pic1.png}'
content = content.replace(old, new)
fixes += 1
print('11. Figure 3.1 width OK')

# Save
with open(r'd:\HealthAgent\docs\thesis.tex', 'w', encoding='utf-8') as f:
    f.write(content)

final = content.count('\n')
print(f'\nFixes applied: {fixes}')
print(f'Lines: {orig} -> {final}')
