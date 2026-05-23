#!/usr/bin/env python3
"""Final aggressive pass — target ~28-30 genuinely essential dashes."""
import re

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

orig_count = content.count('——')
print(f'Starting: {orig_count}')
fixes = 0

replacements = [
    # L258: "判断图片类型——七段数码管LCD图片直达VLM" -> ：
    ('分类器先判断图片类型——七段数码管LCD图片直达VLM做端到端识别（跳过OCR这一步），标准字体图片走百度云通用OCR加X坐标聚类完成字段分配',
     '分类器先判断图片类型：七段数码管LCD图片直达VLM做端到端识别（跳过OCR这一步），标准字体图片走百度云通用OCR加X坐标聚类完成字段分配'),

    # L484: "反而是所有方案中最差的（3.3%）——该接口定位" -> ，
    ('百度数字专用OCR（numbers接口）反而是所有方案中最差的（3.3\\%）——该接口定位为通用数字识别',
     '百度数字专用OCR（numbers接口）反而是所有方案中最差的（3.3\\%），该接口定位为通用数字识别'),

    # L484: "控制在3秒的性能约束之内——在所有对比方案中" -> ，
    ('平均耗时1.00秒控制在3秒的性能约束之内——在所有对比方案中准确率最高',
     '平均耗时1.00秒控制在3秒的性能约束之内，在所有对比方案中准确率最高'),

    # L504: "数值检出率是100%——所有图片上的三个数值" -> ，
    ('在标准印刷字体场景下，百度云OCR的数值检出率是100\\%——所有图片上的三个数值全部被正确识别',
     '在标准印刷字体场景下，百度云OCR的数值检出率是100\\%，所有图片上的三个数值全部被正确识别'),

    # L528: "而非诚实返回null——这正是我们坚持" -> ，
    ('VLM在面对不确定输入时仍可能输出"看起来合理"的猜测值而非诚实返回null——这正是我们坚持"识别结果必须经人工确认才入库"的原因',
     'VLM在面对不确定输入时仍可能输出"看起来合理"的猜测值而非诚实返回null，这正是我们坚持"识别结果必须经人工确认才入库"的原因'),

    # L578: "$w = \min(7, N)$——数据不满7天就缩窗使用" -> （）
    ('滑动窗口大小取$w = \\min(7, N)$——数据不满7天就缩窗使用，保证有限数据下也能给出一个初步判断',
     '滑动窗口大小取$w = \\min(7, N)$（数据不满7天就缩窗使用），保证有限数据下也能给出一个初步判断'),

    # L578: "其余情况判为平稳——3\%这个阈值" -> 。3\%这个阈值
    ('其余情况判为平稳——3\\%这个阈值在典型血压值（120--140 mmHg）上大概对应4 mmHg',
     '其余情况判为平稳。3\\%这个阈值在典型血压值（120--140 mmHg）上大概对应4 mmHg'),

    # L641: "整个方案的核心——HOG+SVM分类器决定处理路径" -> ：
    ('分类先行的双通路流水线是整个方案的核心——HOG\\+SVM分类器决定处理路径',
     '分类先行的双通路流水线是整个方案的核心：HOG+SVM分类器决定处理路径'),

    # L641: "失效的边界——问题出在字形层面" -> ：
    ('消融实验明确了OCR在七段数码管上失效的边界——问题出在字形层面而非后处理环节',
     '消融实验明确了OCR在七段数码管上失效的边界：问题出在字形层面而非后处理环节'),

    # L641: "人机协同机制——识别结果回填至" -> ：
    ('录入环节额外设计了人机协同机制——识别结果回填至前端表单供用户逐字段核对',
     '录入环节额外设计了人机协同机制：识别结果回填至前端表单供用户逐字段核对'),

    # L667: "三个核心服务模块——ocr_service、bp_record_service和chat_service——的覆盖率" -> （）
    ('三个核心服务模块——ocr\\_service、bp\\_record\\_service和chat\\_service——的覆盖率都超过90\\%',
     '三个核心服务模块（ocr\\_service、bp\\_record\\_service和chat\\_service）的覆盖率都超过90\\%'),

    # L798: "访问用户B的数据——服务层的二次校验" -> ，
    ('验证了用户A无法通过篡改记录ID来访问用户B的数据——服务层的二次校验将记录的归属user\\_id与JWT中的身份声明逐一比对',
     '验证了用户A无法通过篡改记录ID来访问用户B的数据，服务层的二次校验将记录的归属user\\_id与JWT中的身份声明逐一比对'),

    # L852: "真实用户验证——没有真实用户的反馈" -> ，
    ('当然，前提是经过真实用户验证——没有真实用户的反馈，上述判断均属于待验证的假设',
     '当然，前提是经过真实用户验证，没有真实用户的反馈，上述判断均属于待验证的假设'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        fixes += 1
        print(f'  {fixes}. OK')
    else:
        print(f'  SKIP: {old[:60]}...')

with open(r'd:\HealthAgent\docs\thesis.tex', 'w', encoding='utf-8') as f:
    f.write(content)

new_count = content.count('——')
print(f'\nReplacements: {fixes}')
print(f'Em-dashes: {orig_count} -> {new_count}')

# Show all remaining
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if '——' in line:
        idx = line.find('——')
        ctx = line[max(0,idx-15):min(len(line),idx+55)].strip()
        print(f'  L{i}: ...{ctx}...')
