#!/usr/bin/env python3
"""Final pass: target remaining replaceable dashes with exact context from file."""
import re

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

orig_count = content.count('——')
print(f'Starting: {orig_count}')
fixes = 0

# Exact string replacements verified from Read output
replacements = [
    # L264: "生态绑定更加突出——Omron Connect"
    ('硬件厂商方案的生态绑定更加突出——Omron Connect只兼容欧姆龙蓝牙血压计',
     '硬件厂商方案的生态绑定更加突出，Omron Connect只兼容欧姆龙蓝牙血压计'),

    # L266: "有实用价值——用户日常佩戴"
    ('这一"被动测量"的设计思路有实用价值——用户日常佩戴手表就能自动积累数据',
     '这一"被动测量"的设计思路有实用价值，用户日常佩戴手表就能自动积累数据'),

    # L407: "归属二次校验——将请求资源的"
    ('服务层对每个资源操作执行归属二次校验——将请求资源的user\\_id字段与JWT中的身份声明逐一比对',
     '服务层对每个资源操作执行归属二次校验：将请求资源的user\\_id字段与JWT中的身份声明逐一比对'),

    # L415: "业务实体——用户、血压记录、问诊会话——各自映射为"
    ('系统的业务实体——用户、血压记录、问诊会话——各自映射为一个URL资源路径',
     '系统的业务实体（用户、血压记录、问诊会话）各自映射为一个URL资源路径'),

    # L415: "理解成本——只要知道资源名称"
    ('降低了前端开发者的理解成本——只要知道资源名称就能推断出基本的操作方式',
     '降低了前端开发者的理解成本，只要知道资源名称就能推断出基本的操作方式'),

    # L421: "各类异常——网络错误显示"
    ('统一的错误格式使得前端的Axios拦截器能够集中处理各类异常——网络错误显示通用提示后自动重试',
     '统一的错误格式使得前端的Axios拦截器能够集中处理各类异常：网络错误显示通用提示后自动重试'),

    # L439: "杂乱排列的——血压值、时间戳"
    ('OCR返回的结果是杂乱排列的——血压值、时间戳、电池标志、记忆编号全部混在一起',
     'OCR返回的结果是杂乱排列的，血压值、时间戳、电池标志、记忆编号全部混在一起'),

    # L439: "保留边界框高度不低于中位数70%的识别结果——血压读数是屏幕上最大的数字"
    ('只保留边界框高度不低于中位数70\\%的识别结果——血压读数是屏幕上最大的数字',
     '只保留边界框高度不低于中位数70\\%的识别结果（血压读数是屏幕上最大的数字，通常占屏幕高度30\\%--40\\%，而时间戳和电池标志的字号明显更小）'),

    # Actually the above is too long. Let me use a shorter unique fragment.
    # L439: "从小到大排列——家用血压计的屏幕布局"
    ('将保留的数值按纵坐标从小到大排列——家用血压计的屏幕布局较为固定',
     '将保留的数值按纵坐标从小到大排列（家用血压计的屏幕布局较为固定，收缩压在上、舒张压居中、心率在下），排序后按位置分配字段'),

    # L439: "则丢弃$v_{dia}$——因为从生理学定义上"
    ('则丢弃$v_{dia}$——因为从生理学定义上收缩压必须严格大于舒张压',
     '则丢弃$v_{dia}$，因为从生理学定义上收缩压必须严格大于舒张压'),

    # L439: "OCR主通路——使用百度云通用OCR接口"
    ('如果分类为非LCD（App界面、打印标签等），则走OCR主通路——使用百度云通用OCR接口',
     '如果分类为非LCD（App界面、打印标签等），则走OCR主通路：使用百度云通用OCR接口'),

    # L439: "LCD直达VLM路径——不再调用百度云OCR" → KEEP (important routing explanation)

    # L504: "X坐标聚类——将X坐标...心率）——字段分配的准确率"
    # Two dashes in one sentence
    ('通过引入X坐标聚类——将X坐标相近的token归为"主列"（收缩压+舒张压），X坐标明显偏离的token识别为"侧栏"（心率）——字段分配的准确率从33.3\\%提升到了100\\%',
     '通过引入X坐标聚类（将X坐标相近的token归为"主列"，即收缩压+舒张压；X坐标明显偏离的token识别为"侧栏"，即心率），字段分配的准确率从33.3\\%提升到了100\\%'),

    # L528: VLM limitation
    ('但在边缘情况下（反光严重、拍糊了、屏幕坏了）是防止模型"合理编造"的关键防线',
     '但在边缘情况下（反光严重、拍糊了、屏幕坏了）是防止模型"合理编造"的关键防线'),  # no change, verify

    # L484 area: check what's there
    # From the remaining dashes: "训练数据的字形分布与血压计屏幕之间存在系统性的不匹配" — already used : earlier
    # This is L484 from grep. Let me check by reading.

    # L633: "三条正则规则——引用格式检测"
    ('对每条回答依次运行三条正则规则——引用格式检测匹配[n]编号模式',
     '对每条回答依次运行三条正则规则：引用格式检测匹配[n]编号模式'),

    # L708: "这一危险请求——后面这个拒绝"
    ('并且明确拒绝了"加倍服药"这一危险请求——后面这个拒绝在实际场景中可能比前面的建议更重要',
     '并且明确拒绝了"加倍服药"这一危险请求，后面这个拒绝在实际场景中可能比前面的建议更重要'),

    # L788: "Token数量影响——数据解读类问题"
    ('主要受模型输出的Token数量影响——数据解读类问题（Q1--Q3）的回答通常较长',
     '主要受模型输出的Token数量影响，数据解读类问题（Q1--Q3）的回答通常较长'),

    # L798: "安全测试" area - check what dash is there
    # From remaining: "将记录的归属user_id与JWT中的身份声明逐一比对，越权访问一律返回404" — this line has the same text as 407. The dash at L798 might be different.
    # Let me check what the dash is at L798

    # L641: "双通路流水线是整个方案的核心——HOG+SVM分类器"
    ('分类先行的双通路流水线是整个方案的核心——HOG\\+SVM分类器决定处理路径',
     '分类先行的双通路流水线是整个方案的核心：HOG+SVM分类器决定处理路径'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        fixes += 1
        print(f'  {fixes}. OK: {old[:50]}...')
    else:
        print(f'  SKIP: {old[:50]}...')

# Save
with open(r'd:\HealthAgent\docs\thesis.tex', 'w', encoding='utf-8') as f:
    f.write(content)

new_count = content.count('——')
print(f'\nReplacements: {fixes}')
print(f'Em-dashes: {orig_count} -> {new_count} (removed {orig_count - new_count})')
