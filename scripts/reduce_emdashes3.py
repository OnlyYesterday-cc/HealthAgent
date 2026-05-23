#!/usr/bin/env python3
"""Third pass: aggressive reduction — target ~30 genuinely essential dashes."""
import re

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

orig_count = content.count('——')
print(f'Starting em-dash count: {orig_count}')
fixes = 0

# ============================================================
# Keep only ~30-35. Replace all others aggressively.
# KEEP criteria: dramatic emphasis, key insight/turning point,
#   security rationale, honest self-assessment, key distinction
# ============================================================

replacements = [
    # === Ch1 ===
    # Line 228: KEEP "27.9%——四个成年人里就有一个" (dramatic)
    # Line 244: KEEP "显著下降——这是项目初期" (turning point)
    # Line 252: KEEP "超出最初预期——反复试验后确认" (result emphasis)
    # Line 258: KEEP "核心洞察...——既然已知" (key insight)

    # Line 258: "判断图片类型——七段数码管LCD图片直达VLM" -> ：
    ('HOG\\+SVM）分类器先判断图片类型——七段数码管LCD图片直达VLM做端到端识别',
     'HOG+SVM）分类器先判断图片类型：七段数码管LCD图片直达VLM做端到端识别'),

    # === Ch2 ===
    # Line 264: "核心思路是聚合——通过HealthKit" -> ：
    ('Apple Health的核心思路是聚合——通过HealthKit',
     'Apple Health的核心思路是聚合：通过HealthKit'),

    # Line 266: "比较薄弱——通常只提供" -> ，
    ('在数据解读方面普遍比较薄弱——通常只提供',
     '在数据解读方面普遍比较薄弱，通常只提供'),

    # Line 294: KEEP "并不均匀——OCR模块所占用的精力最多"
    # Line 340: KEEP "不及简单滑动平均——模型越复杂"

    # Line 344: "Django功能全面——ORM" -> ：
    ('Django功能全面——ORM、管理后台、认证系统均内置',
     'Django功能全面（ORM、管理后台、认证系统均内置）'),

    # === Ch3 ===
    # Line 376 area - user_id isolation dash (should already be replaced)
    # Let me check what's left

    # Line 407: bcrypt hash dash - it was already replaced. Let me check remaining

    # Line 401 area: remaining dash
    # Actually let me check from grep what's at these lines

    # === Ch4 ===
    # Line 415 area: version embedding dash
    ('版本号嵌入URL路径而非请求头——是为了让API版本与代码分支直接对应',
     '版本号嵌入URL路径而非请求头，是为了让API版本与代码分支直接对应'),

    # Line 417: KEEP "长连接而非WebSocket——后者"
    # Line 419: KEEP "限流机制——因系统尚未部署至公网"

    # Line 421: error response dash
    ('所有异常在接口层被统一捕获——转换为固定格式的JSON错误响应',
     '所有异常在接口层被统一捕获，转换为固定格式的JSON错误响应'),

    # Line 439: "不足1毫秒——不产生任何API调用开销" -> ，
    ('本地推理耗时不足1毫秒——不产生任何API调用开销',
     '本地推理耗时不足1毫秒，不产生任何API调用开销'),

    # Line 484: "准确率最高，且仅比最快的纯OCR方案多约0.36秒——" Check the actual text
    # This is in table analysis section, let me check

    # Line 486: KEEP "端到端识别——OCR主通路在此路径上完全不被调用"
    # Line 504: OCR ablation analysis dash
    ('OCR在字形层面就失效了——七段数码管的字形分布',
     'OCR在字形层面就失效了：七段数码管的字形分布'),  # This is line 506 actually

    # Line 528: X coordinate limitation
    ('一是X坐标聚类的假设不一定在所有界面布局上都成立——如果某个App',
     '一是X坐标聚类的假设不一定在所有界面布局上都成立，如果某个App'),

    # Line 568: KEEP "刻意为之——防止攻击者"

    # Line 578: 滑动窗口 dash
    ('数据满足最低3天要求后，滑动窗口大小取$w = \\min(7, N)$——数据不满7天就缩窗使用',
     '数据满足最低3天要求后，滑动窗口大小取$w = \\min(7, N)$（数据不满7天就缩窗使用）'),

    # Line 614: Six safety rules — each "——" in enumeration
    ('第一条是角色定位——"你是一个健康助手',
     '第一条是角色定位："你是一个健康助手'),
    ('第二条是强制引用——"回答中所有事实性陈述',
     '第二条是强制引用："回答中所有事实性陈述'),
    ('第三条是禁止剂量建议——"绝对不要推荐具体药物',
     '第三条是禁止剂量建议："绝对不要推荐具体药物'),
    ('第四条是禁止确定性诊断——"不得使用',
     '第四条是禁止确定性诊断："不得使用'),
    ('第五条是诚实边界——"如果知识库里没有相关信息',
     '第五条是诚实边界："如果知识库里没有相关信息'),
    ('最后一条是强制免责声明——"每轮回答末尾必须加上',
     '最后一条是强制免责声明："每轮回答末尾必须加上'),

    # Line 633: 安全指标验证
    ('安全指标的验证如果每次都靠人工逐条检查，既耗时又容易遗漏——为此我们',
     '安全指标的验证如果每次都靠人工逐条检查，既耗时又容易遗漏，为此我们'),

    # Line 641: OCR模块 dash
    ('OCR模块占据最多篇幅——因为它面临的问题在三个模块中最为困难',
     'OCR模块占据最多篇幅，因为它面临的问题在三个模块中最为困难'),

    # Line 643: KEEP "数据量尚不足以进行趋势分析——在健康场景下"

    # Line 645: RAG summary
    ('SSE逐字推给前端、自动评测脚本做安全回归——每个环节的选型都绕不开同一个问题',
     'SSE逐字推给前端、自动评测脚本做安全回归。每个环节的选型都绕不开同一个问题'),

    # === Ch5 ===
    # Line 661: KEEP "交互问题较多——特别是"
    # Line 665: "约11秒——可满足快速回归测试的需求" -> ，
    ('全部86个用例在验收阶段通过，累计执行时间约11秒——可满足快速回归测试的需求',
     '全部86个用例在验收阶段通过，累计执行时间约11秒，可满足快速回归测试的需求'),

    # Line 667: KEEP "三个核心服务模块——ocr_service、bp_record_service和chat_service——的覆盖率" (enumeration)
    # Line 673: KEEP "时间约束下的取舍——在前后端并行推进"

    # Line 706: KEEP "基线LLM——本系统的评测结果与该Meta分析"
    # Line 708: "模型的表现是符合预期的——它明确说了" -> ，
    ('模型的表现是符合预期的——它明确说了',
     '模型的表现是符合预期的，它明确说了'),

    # Line 741: KEEP "OCR漏检——该问题已在VLM兜底机制中有所缓解"
    # Line 764: KEEP "有意选择的参数——该延迟在用户体验可接受范围内"

    # Line 788: "设计约束——用户在对话界面" -> ，
    ('SSE首Token的P95延迟为1.50秒，远低于3秒的设计约束——用户在对话界面',
     'SSE首Token的P95延迟为1.50秒，远低于3秒的设计约束，用户在对话界面'),

    # Line 792: "十余秒即可完成回归检测——对于需要频繁迭代" -> ；
    ('十余秒即可完成回归检测——对于需要频繁迭代OCR流水线和Prompt模板的开发节奏而言',
     '十余秒即可完成回归检测，对于需要频繁迭代OCR流水线和Prompt模板的开发节奏而言'),

    # Line 798: 安全测试 dash
    ('越权访问一律返回404（刻意不用403，原因在3.3节已说明）',
     '越权访问一律返回404（刻意不用403，原因在3.3节已说明）'),  # no change, just verifying no dash

    # === Ch6 ===
    # Line 824: KEEP "不足也需要正视——有些是受限于"
    # Line 826: KEEP "还是不够——用二项分布估算"
    # Line 828: "不易被替代的优点——结果高度透明" -> ：
    ('且有一个不易被替代的优点——结果高度透明，易于理解',
     '且有一个不易被替代的优点：结果高度透明，易于理解'),

    # Line 830: KEEP "本质上是'软'的——它们是要求大模型遵守的规则"
    # Line 832: KEEP "适配也未实现——对于一个目标用户"
    # Line 834: KEEP "使用体验和反馈——目前仍缺少这一环节"
    # Line 838: KEEP "继续推进——按优先级排列"
    # Line 840: KEEP "标准化评测基准——没有足够规模的测试集"
    # Line 850: KEEP "规则引擎——LLM生成的文本"

    # Line 852: "聊天获建议——这三个环节" -> ：
    ('聊天获建议——这三个环节串联起来，构成了从数据采集到行动决策的完整小闭环',
     '聊天获建议，这三个环节串联起来，构成了从数据采集到行动决策的完整小闭环'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        fixes += 1
        # Print first 40 chars of old for tracking
        short = old[:50].replace('\n', ' ')
        print(f'  {fixes}. {short}...')
    else:
        short = old[:50].replace('\n', ' ')
        print(f'  SKIP: {short}...')

# Save
with open(r'd:\HealthAgent\docs\thesis.tex', 'w', encoding='utf-8') as f:
    f.write(content)

new_count = content.count('——')
print(f'\nTotal replacements: {fixes}')
print(f'Em-dashes: {orig_count} -> {new_count} (removed {orig_count - new_count})')

# Show all remaining dashes with context
print('\n=== REMAINING DASHES ===')
lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if '——' in line:
        # Find the dash and show surrounding context
        idx = line.find('——')
        start = max(0, idx - 20)
        end = min(len(line), idx + 50)
        ctx = line[start:end].strip()
        print(f'  L{i}: ...{ctx}...')
