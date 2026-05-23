#!/usr/bin/env python3
"""
Reduce excessive em-dashes (——) in thesis.tex.
Keeps ~35 genuinely useful dashes (dramatic emphasis, key insights, turning points)
Replaces ~110+ unnecessary ones with commas, colons, periods, or semicolons.
"""
import re

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

orig_count = content.count('——')
print(f'Original em-dash count: {orig_count}')
fixes = 0

# ============================================================
# CHAPTER 1: 绪论 (original ~26 dashes, target ~6-8)
# ============================================================

# Line 228: "约27.9\%——四个成年人里就有一个" → KEEP (dramatic emphasis)
# Line 228: "风险——收缩压每降低10 mmHg" → ：
old = '可显著降低心脑血管事件风险——收缩压每降低10 mmHg，主要心血管事件风险约下降20\\%'
new = '可显著降低心脑血管事件风险：收缩压每降低10 mmHg，主要心血管事件风险约下降20\\%'
if old in content:
    content = content.replace(old, new); fixes += 1; print('1. 风险—— → ：')

# Line 230: "更为突出——视力衰退导致" → ，
old = '对老年用户而言这一问题更为突出——视力衰退导致屏幕读数辨识困难'
new = '对老年用户而言这一问题更为突出，视力衰退导致屏幕读数辨识困难'
if old in content:
    content = content.replace(old, new); fixes += 1; print('2. 更为突出—— → ，')

# Line 230: "临床含义——某次测量值偏高" → ：
old = '不解释曲线背后的临床含义——某次测量值偏高是否需要警惕？近期减少食盐摄入是否已产生效果？'
new = '不解释曲线背后的临床含义：某次测量值偏高是否需要警惕？近期减少食盐摄入是否已产生效果？'
if old in content:
    content = content.replace(old, new); fixes += 1; print('3. 临床含义—— → ：')

# Line 242: "典型代表——1985年始于" → ：
old = 'Tesseract\\textsuperscript{[3]}是这一演进路线上的典型代表——1985年始于HP实验室'
new = 'Tesseract\\textsuperscript{[3]}是这一演进路线上的典型代表：1985年始于HP实验室'
if old in content:
    content = content.replace(old, new); fixes += 1; print('4. 典型代表—— → ：')

# Line 244: "显著下降——这是项目初期" → KEEP (turning point)

# Line 246: "差异相当明显——上午自然光下" → ：
old = '同一数值在不同照片中的笔画完整性差异相当明显——上午自然光下的"8"清晰可辨'
new = '同一数值在不同照片中的笔画完整性差异相当明显：上午自然光下的"8"清晰可辨'
if old in content:
    content = content.replace(old, new); fixes += 1; print('5. 差异相当明显—— → ：')

# Line 248: "远超预期——部分照片中" → ：
old = '所得照片在亮度、角度、清晰度上的差异远超预期——部分照片中屏幕区域仅占画面的六分之一不到'
new = '所得照片在亮度、角度、清晰度上的差异远超预期，部分照片中屏幕区域仅占画面的六分之一不到'
if old in content:
    content = content.replace(old, new); fixes += 1; print('6. 远超预期—— → ，')

# Line 250: "混淆问题——屏幕上除" → ：
old = '第三个层面是屏幕信息的混淆问题——屏幕上除收缩压、舒张压、心率之外，还包含时间戳'
new = '第三个层面是屏幕信息的混淆问题：屏幕上除收缩压、舒张压、心率之外，还包含时间戳'
if old in content:
    content = content.replace(old, new); fixes += 1; print('7. 混淆问题—— → ：')

# Line 252: "超出最初预期——反复试验后确认" → KEEP (result emphasis)

# Line 256: "VLM）——GPT-4V" → ：
old = '另一条路线是多模态视觉大模型（Vision-Language Model, VLM）——GPT-4V、通义千问VL、Gemini Pro Vision等不仅识别数字形态'
new = '另一条路线是多模态视觉大模型（Vision-Language Model, VLM）：GPT-4V、通义千问VL、Gemini Pro Vision等不仅识别数字形态'
if old in content:
    content = content.replace(old, new); fixes += 1; print('8. VLM）—— → ：')

# Line 258: "核心洞察是...——既然已知" → KEEP (key insight)

# Line 264: "核心思路是聚合——通过HealthKit" → ：
old = 'Apple Health的核心思路是聚合——通过HealthKit把iPhone、Apple Watch和第三方设备数据汇总到一起'
new = 'Apple Health的核心思路是聚合：通过HealthKit把iPhone、Apple Watch和第三方设备数据汇总到一起'
if old in content:
    content = content.replace(old, new); fixes += 1; print('9. 核心思路是聚合—— → ：')

# Line 266: "比较薄弱——通常只提供" → ：
old = '在数据解读方面普遍比较薄弱——通常只提供"本月血压偏高次数：X次"等简单统计'
new = '在数据解读方面普遍比较薄弱，通常只提供"本月血压偏高次数：X次"等简单统计'
if old in content:
    content = content.replace(old, new); fixes += 1; print('10. 比较薄弱—— → ，')

# Line 280: "不容忽视的问题——以高度自信的语气" → ：
old = '大模型存在一个不容忽视的问题——以高度自信的语气生成不实信息'
new = '大模型存在一个不容忽视的问题：以高度自信的语气生成不实信息'
if old in content:
    content = content.replace(old, new); fixes += 1; print('11. 不容忽视的问题—— → ：')

# Line 284: "统计平均——它天然倾向于" → ，
old = '通用模型的"经验"来自海量文本的统计平均——它天然倾向于给出普适性建议'
new = '通用模型的"经验"来自海量文本的统计平均，它天然倾向于给出普适性建议'
if old in content:
    content = content.replace(old, new); fixes += 1; print('12. 统计平均—— → ，')

# Line 286: "成本可控的解决路径——核心思路并不复杂" → 。其
old = '为上述三个问题提供了一条工程上可行且成本可控的解决路径。核心思路并不复杂'
new = '为上述三个问题提供了一条工程上可行且成本可控的解决路径。其核心思路并不复杂'
if old in content:
    content = content.replace(old, new); fixes += 1; print('13. 解决路径。—— → 。其')

# Line 288: "技术决策之一——理由较为实际" → ，
old = '选择RAG而非微调，是项目中最早确定的几个技术决策之一，理由较为实际'
# Check if it's currently with dash
old_dash = '选择RAG而非微调，是项目中最早确定的几个技术决策之一——理由较为实际'
if old_dash in content:
    content = content.replace(old_dash, old); fixes += 1; print('14. 技术决策之一—— → ，')

# Line 294: "并不均匀——OCR模块所占用的精力最多" → KEEP

# Line 296: "标准字体界面——LCD直接路由至" → ：
old = '分类器先判断图片是七段数码管LCD屏幕还是标准字体界面——LCD直接路由至通义千问VLM进行端到端识别'
new = '分类器先判断图片是七段数码管LCD屏幕还是标准字体界面：LCD直接路由至通义千问VLM进行端到端识别'
if old in content:
    content = content.replace(old, new); fixes += 1; print('15. 标准字体界面—— → ：')

# Line 298: "两块动态信息——用户最近14天" → ：
old = 'Prompt中嵌入两块动态信息——用户最近14天的血压概况和检索到的知识库片段'
new = 'Prompt中嵌入两块动态信息：用户最近14天的血压概况和检索到的知识库片段'
if old in content:
    content = content.replace(old, new); fixes += 1; print('16. 动态信息—— → ：')

# Line 300: "端到端的数据链路——从采集、趋势分析到可视化看板" → ：
old = '第三块是端到端的数据链路——从采集、趋势分析到可视化看板'
new = '第三块是端到端的数据链路：从采集、趋势分析到可视化看板'
if old in content:
    content = content.replace(old, new); fixes += 1; print('17. 数据链路—— → ：')

# ============================================================
# CHAPTER 2: 相关技术 (original ~16 dashes, target ~3-4)
# ============================================================

# Line 320: Uses "--" for ranges (not em-dashes) — skip

# Line 322: Check - "最有效手段——" maybe not in the text? Let me check what's at line 322.
# Actually line 322 is "...这在项目初期反复验证后确认的事实..." or similar. Let me verify.

# Line 326: "自回归的——每一步根据上文" → ：
old = '生成是逐Token自回归的——每一步根据上文计算下一个Token的概率分布'
new = '生成是逐Token自回归的：每一步根据上文计算下一个Token的概率分布'
if old in content:
    content = content.replace(old, new); fixes += 1; print('18. 自回归的—— → ：')

# Line 328: "不可回避的问题——幻觉" → ：
old = '但将通用大模型直接应用于医疗场景存在一个不可回避的问题——幻觉。模型会以高度自信的语气生成不实信息'
new = '但将通用大模型直接应用于医疗场景存在一个不可回避的问题：幻觉。模型会以高度自信的语气生成不实信息'
if old in content:
    content = content.replace(old, new); fixes += 1; print('19. 不可回避的问题—— → ：')

# Line 332: "安全层面的确定性——在医疗场景下" → ；
old = '但换来了安全层面的确定性——在医疗场景下，这一取舍是合理的'
new = '但换来了安全层面的确定性；在医疗场景下，这一取舍是合理的'
if old in content:
    content = content.replace(old, new); fixes += 1; print('20. 确定性—— → ；')

# Line 336: "轻量级策略——滑动平均配合线性回归" → ：
old = '血压趋势判定上，采用了轻量级策略——滑动平均配合线性回归，未引入复杂模型'
new = '血压趋势判定上，采用了轻量级策略：滑动平均配合线性回归，未引入复杂模型'
if old in content:
    content = content.replace(old, new); fixes += 1; print('21. 轻量级策略—— → ：')

# Line 338: "简洁的平滑方法之一——以固定大小的窗口" → ：
old = '简单滑动平均（Simple Moving Average, SMA）是最为简洁的平滑方法之一——以固定大小的窗口沿序列滑动'
new = '简单滑动平均（Simple Moving Average, SMA）是最为简洁的平滑方法之一：以固定大小的窗口沿序列滑动'
if old in content:
    content = content.replace(old, new); fixes += 1; print('22. 平滑方法—— → ：')

# Line 338: "整体走向——上升、下降，或保持平稳" → ：
old = '斜率的符号与绝对值大小即可大致反映血压的整体走向——上升、下降，或保持平稳'
new = '斜率的符号与绝对值大小即可大致反映血压的整体走向：上升、下降，或保持平稳'
if old in content:
    content = content.replace(old, new); fixes += 1; print('23. 整体走向—— → ：')

# Line 340: "不及简单滑动平均——模型越复杂" → KEEP (summarizing contrast)

# Line 344: "介于二者之间——借助Python类型注解" → ：
old = 'FastAPI恰好介于二者之间——借助Python类型注解和Pydantic v2自动生成请求校验'
new = 'FastAPI恰好介于二者之间：借助Python类型注解和Pydantic v2自动生成请求校验'
if old in content:
    content = content.replace(old, new); fixes += 1; print('24. 介于二者之间—— → ：')

# Line 346: "务实的选择——MySQL和PostgreSQL需要" → ：
old = '但在单机部署场景下是一个务实的选择——MySQL和PostgreSQL需要独立的服务进程'
new = '但在单机部署场景下是一个务实的选择：MySQL和PostgreSQL需要独立的服务进程'
if old in content:
    content = content.replace(old, new); fixes += 1; print('25. 务实的选择—— → ：')

# Line 348: "主要是因为两点——Ant Design 5和ECharts" → ：
old = '最终选React主要是因为两点——Ant Design 5和ECharts在React生态中的封装最成熟'
new = '最终选React主要是因为两点：Ant Design 5和ECharts在React生态中的封装最成熟'
if old in content:
    content = content.replace(old, new); fixes += 1; print('26. 因为两点—— → ：')

# Line 350: "寻求平衡——若仅使用一个长期Token" → ：
old = '采用双Token而非单Token长期有效的设计，主要是在安全与体验之间寻求平衡——若仅使用一个长期Token，泄露将导致整个账户暴露'
new = '采用双Token而非单Token长期有效的设计，主要是在安全与体验之间寻求平衡：若仅使用一个长期Token，泄露将导致整个账户暴露'
if old in content:
    content = content.replace(old, new); fixes += 1; print('27. 寻求平衡—— → ：')

# Line 350: "取得平衡——cost factor为12时" → ，
old = '该参数在安全性与登录延迟之间取得了平衡——cost factor为12时单次哈希约250ms'
new = '该参数在安全性与登录延迟之间取得了平衡，cost factor为12时单次哈希约250ms'
if old in content:
    content = content.replace(old, new); fixes += 1; print('28. 取得平衡—— → ，')

# Line 354: "轻量优先"的策略——以滑动平均" → ：
old = '确定了"轻量优先"的策略——以滑动平均配合线性回归为基线'
new = '确定了"轻量优先"的策略：以滑动平均配合线性回归为基线'
if old in content:
    content = content.replace(old, new); fixes += 1; print('29. 轻量优先策略—— → ：')

# ============================================================
# CHAPTER 3: 需求分析与系统设计 (original ~24 dashes, target ~5-6)
# ============================================================

# Line 362: "三个环节的断裂" - this paragraph uses "——" three times in one sentence!
old = ('在家庭血压管理场景中，用户面临的核心问题可概括为三个环节的断裂：'
       '测量环节的数据记录阻力大（手写易丢失、手动录入繁琐）、'
       '回顾环节的趋势解读能力弱（仅有数值列表而无分析）、'
       '咨询环节的信息获取渠道杂（网络搜索质量参差不齐）')
if old not in content:
    # Try the version with dashes
    old_dash = ('在家庭血压管理场景中，用户面临的核心问题可概括为三个环节的断裂——'
                '测量环节的数据记录阻力大（手写易丢失、手动录入繁琐）、'
                '回顾环节的趋势解读能力弱（仅有数值列表而无分析）、'
                '咨询环节的信息获取渠道杂（网络搜索质量参差不齐）')
    if old_dash in content:
        content = content.replace(old_dash, old); fixes += 1; print('30. 三个环节的断裂—— → ：')

# Line 366: Three dashes for the three design principles
# "人机协同闭环——OCR识别结果不直接入库" → ：
old = '第一条是"机器先认、人来把关"的人机协同闭环——OCR识别结果不直接入库'
new = '第一条是"机器先认、人来把关"的人机协同闭环：OCR识别结果不直接入库'
if old in content:
    content = content.replace(old, new); fixes += 1; print('31. 人机协同闭环—— → ：')

old = '第二条是"数据不足时如实告知优于强行推断"的诚实策略——趋势判定算法在有效记录不足3天时直接返回'
new = '第二条是"数据不足时如实告知优于强行推断"的诚实策略：趋势判定算法在有效记录不足3天时直接返回'
if old in content:
    content = content.replace(old, new); fixes += 1; print('32. 诚实策略—— → ：')

old = '第三条是"安全约束嵌入交互流程"的设计理念——医疗合规要求（免责声明、禁止诊断等）不只写在系统指令中'
new = '第三条是"安全约束嵌入交互流程"的设计理念：医疗合规要求（免责声明、禁止诊断等）不只写在系统指令中'
if old in content:
    content = content.replace(old, new); fixes += 1; print('33. 设计理念—— → ：')

# Line 370: "降低录入阻力——手动输入三个数值" → ：
old = '对这类用户而言，最核心的需求是降低录入阻力——手动输入三个数值（收缩压、舒张压、心率）对年轻人仅需数秒'
new = '对这类用户而言，最核心的需求是降低录入阻力：手动输入三个数值（收缩压、舒张压、心率）对年轻人仅需数秒'
if old in content:
    content = content.replace(old, new); fixes += 1; print('34. 降低录入阻力—— → ：')

# Line 376: Multiple dashes, let me check the actual content
# "OCR从上传到返回结果不超过3秒——该数值基于用户对拍照上传等待时间的可接受上限估算"
old = 'OCR从上传到返回结果不超过3秒——该数值基于用户对拍照上传等待时间的可接受上限估算'
new = 'OCR从上传到返回结果不超过3秒，该数值基于用户对拍照上传等待时间的可接受上限估算'
if old in content:
    content = content.replace(old, new); fixes += 1; print('35. 3秒—— → ，')

# "跨用户访问统一返回HTTP 404而非403——因为403会暴露"
old = '跨用户访问统一返回HTTP 404而非403，因为403会暴露'
old_dash = '跨用户访问统一返回HTTP 404而非403——因为403会暴露'
if old_dash in content:
    content = content.replace(old_dash, old); fixes += 1; print('36. 404而非403—— → ，')

# Line 382: "同一个SQLite文件——不需要单独部署什么中间件" → ，
old = '两者都放在同一个SQLite文件——不需要单独部署什么中间件，备份也很简单'
new = '两者都放在同一个SQLite文件中，不需要单独部署什么中间件，备份也很简单'
if old in content:
    content = content.replace(old, new); fixes += 1; print('37. SQLite文件—— → 中，')

# Line 401: "用来计算年龄——后面做个性化血压阈值判定" → ，
old = 'birth\\_date字段用来计算年龄——后面做个性化血压阈值判定的差异化建议时，年龄是一个重要输入'
new = 'birth\\_date字段用来计算年龄，后面做个性化血压阈值判定的差异化建议时，年龄是一个重要输入'
if old in content:
    content = content.replace(old, new); fixes += 1; print('38. 计算年龄—— → ，')

old2 = 'birth_date字段用来计算年龄——后面做个性化血压阈值判定的差异化建议时，年龄是一个重要输入'
new2 = 'birth_date字段用来计算年龄，后面做个性化血压阈值判定的差异化建议时，年龄是一个重要输入'
if old2 in content:
    content = content.replace(old2, new2); fixes += 1; print('38b. 计算年龄—— → ，')

# Line 407: "该参数下单次哈希约250毫秒——在登录延迟可接受的范围内" → ，
old = '用户密码经bcrypt算法（cost factor=12）哈希后存储——该参数下单次哈希约250毫秒'
new = '用户密码经bcrypt算法（cost factor=12）哈希后存储，该参数下单次哈希约250毫秒'
if old in content:
    content = content.replace(old, new); fixes += 1; print('39. 哈希后存储—— → ，')

# Line 415: resource path versioning dash
old = "版本号嵌入URL路径而非请求头，是为了让API版本与代码分支直接对应"
old_dash = "版本号嵌入URL路径而非请求头——是为了让API版本与代码分支直接对应"
if old_dash in content:
    content = content.replace(old_dash, old); fixes += 1; print('40. 请求头—— → ，')

# Line 417: "SSE长连接而非WebSocket——后者在此场景下全双工能力过剩" → KEEP (contrast)
# Line 419: "服务端未实现限流机制——因系统尚未部署至公网" → KEEP (explanation)

# Line 421: This section about error responses - let me check
old = '所有异常在接口层被统一捕获，转换为固定格式的JSON错误响应'
old_dash = '所有异常在接口层被统一捕获——转换为固定格式的JSON错误响应'
if old_dash in content:
    content = content.replace(old_dash, old); fixes += 1; print('41. 统一捕获—— → ，')

# ============================================================
# CHAPTER 4: 关键模块实现 (original ~47 dashes, target ~12-14)
# ============================================================

# Line 439: "不足1毫秒——不产生任何API调用开销" → KEEP (key advantage)
# Line 439: "下一步——分类完成后进入路径路由" → hmm, need to check exact text

# Line 484: "准确率最高，且仅比最快的纯OCR方案多约0.36秒——" → KEEP? Let me check
# Actually this is from the performance comparison. KEEP.

# Line 486: "直接路由至VLM完成端到端识别——OCR主通路在此路径上完全不被调用" → KEEP

# Line 504: OCR failure summary
old = '但OCR在字形层面就失效了——七段数码管的字形分布与OCR训练语料之间存在系统性的不匹配'  # Line 506
# KEEP - important conclusion

# Line 528: "是X坐标聚类的假设不一定在所有界面布局上都成立——如果某个App" → ，
old = '一是X坐标聚类的假设不一定在所有界面布局上都成立——如果某个App把心率放在收缩压正下方而非右侧'
new = '一是X坐标聚类的假设不一定在所有界面布局上都成立，如果某个App把心率放在收缩压正下方而非右侧'
if old in content:
    content = content.replace(old, new); fixes += 1; print('42. 都成立—— → ，')

# Line 534: "不仅取决于VLM模型本身的视觉理解能力，更取决于Prompt如何引导模型的注意力分配和输出格式——"
# This is a topic sentence for a subsubsection. KEEP? No, replace.
old = '不仅取决于VLM模型本身的视觉理解能力，更取决于Prompt如何引导模型的注意力分配和输出格式。本节说明VLM Prompt的三层结构设计和背后的考量'
old_dash = '不仅取决于VLM模型本身的视觉理解能力，更取决于Prompt如何引导模型的注意力分配和输出格式——本节说明VLM Prompt的三层结构设计和背后的考量'
if old_dash in content:
    content = content.replace(old_dash, old); fixes += 1; print('43. 输出格式—— → 。')

# Line 547: "置信度字段使得上游模块能够区分" → the dash in this context
old = '置信度字段使得上游模块能够区分"模型很确定的值"和"模型在猜测的值"——为后续的人机协同审核提供优先级信号'
new = '置信度字段使得上游模块能够区分"模型很确定的值"和"模型在猜测的值"，为后续的人机协同审核提供优先级信号'
if old in content:
    content = content.replace(old, new); fixes += 1; print('44. 猜测的值"—— → "，')

# Line 549: "作用不明显——所有字段都清晰可辨时模型自然不会触发——但在边缘情况下" → two dashes
old = '这些负向约束在常规图片上作用不明显——所有字段都清晰可辨时模型自然不会触发——但在边缘情况下'
new = '这些负向约束在常规图片上作用不明显（所有字段都清晰可辨时模型自然不会触发），但在边缘情况下'
if old in content:
    content = content.replace(old, new); fixes += 1; print('45. 作用不明显...不触发—— → （...）')

# Line 560: caption dash
old = r'\caption{拍照录入界面——左侧为OCR图像上传与识别区，右侧为数据核对与保存表单}'
new = r'\caption{拍照录入界面：左侧为OCR图像上传与识别区，右侧为数据核对与保存表单}'
if old in content:
    content = content.replace(old, new); fixes += 1; print('46. 拍照录入界面—— → ：')

# Line 568: "刻意为之——防止攻击者" → KEEP

# Line 578: "趋势判定算法" — let me check
# Actually let me look at what's around line 578
old = '数据满足最低3天要求后，滑动窗口大小取$w = \\min(7, N)$——数据不满7天就缩窗使用'
new = '数据满足最低3天要求后，滑动窗口大小取$w = \\min(7, N)$（数据不满7天就缩窗使用）'
if old in content:
    content = content.replace(old, new); fixes += 1; print('47. 缩窗使用—— → （）')

# Line 582: "底部ECharts双Y轴折线图是看点——左轴表示mmHg"
old = '底部ECharts双Y轴折线图是看点——左轴表示mmHg（收缩压和舒张压），右轴表示bpm（心率）'
new = '底部ECharts双Y轴折线图是看点：左轴表示mmHg（收缩压和舒张压），右轴表示bpm（心率）'
if old in content:
    content = content.replace(old, new); fixes += 1; print('48. 是看点—— → ：')

# Line 587: caption
old = r'\caption{首页看板——包含统计卡片、趋势提示和血压/心率时序图}'
new = r'\caption{首页看板：包含统计卡片、趋势提示和血压/心率时序图}'
if old in content:
    content = content.replace(old, new); fixes += 1; print('49. 首页看板—— → ：')

# Line 594: caption
old = r'\caption{健康数据管理界面——血压/心率记录列表，支持时间筛选与分页浏览}'
new = r'\caption{健康数据管理界面：血压/心率记录列表，支持时间筛选与分页浏览}'
if old in content:
    content = content.replace(old, new); fixes += 1; print('50. 健康数据管理界面—— → ：')

# Line 608: "这一'先检索、再生成'的范式" dash
old = '这一"先检索、再生成"的范式源于Lewis等人'
old_dash_colon = '这一"先检索、再生成"的范式——源于Lewis等人'
if old_dash_colon in content:
    content = content.replace(old_dash_colon, old); fixes += 1; print('51. 的范式—— → 的范式')

# Line 614: Six rules - probably has dashes
# Line 614: "禁止确定性诊断——不得使用" → ：
old = "不得使用'你患有XX病'等表述"
old_dash_diag = "禁止确定性诊断——不得使用'你患有XX病'等表述"
if old_dash_diag in content:
    new_diag = "禁止确定性诊断（不得使用'你患有XX病'等表述）"
    # Actually, these are listed items, let me check the format
    pass

# Line 620:
old = '事件序列分为三种类型——citations事件在LLM开始生成之前就把检索到的引用列表推给前端'
new = '事件序列分为三种类型。首先是citations事件，它在LLM开始生成之前就把检索到的引用列表推给前端'
# This may not match exactly, let me check
old_alt = '事件序列分为三种类型。首先是citations事件'
old_dash_alt = '事件序列分为三种类型——citations事件'
if old_dash_alt in content:
    content = content.replace(old_dash_alt, old_alt); fixes += 1; print('52. 事件序列—— → 。')

# This one: "事件序列分为三种类型——citations事件，它在LLM"
old_v2 = '事件序列分为三种类型：首先是citations事件，它在LLM'
old_v2d = '事件序列分为三种类型——citations事件，它在LLM'
if old_v2d in content:
    content = content.replace(old_v2d, old_v2); fixes += 1; print('52b. 事件序列—— → ：')

# Line 622: "前端方面，我们使用Fetch API配合ReadableStream手动解析SSE流，而不是直接使用浏览器的EventSource接口——原因是EventSource不支持自定义请求头"
old = '而不是直接使用浏览器的EventSource接口——原因是EventSource不支持自定义请求头，无法携带JWT认证信息'
new = '而不是直接使用浏览器的EventSource接口，原因是EventSource不支持自定义请求头，无法携带JWT认证信息'
if old in content:
    content = content.replace(old, new); fixes += 1; print('53. EventSource接口—— → ，')

# Line 627: caption
old = r'\caption{智能问诊界面——左侧为会话列表，右侧为流式对话区域，支持Markdown渲染与引用溯源}'
new = r'\caption{智能问诊界面：左侧为会话列表，右侧为流式对话区域，支持Markdown渲染与引用溯源}'
if old in content:
    content = content.replace(old, new); fixes += 1; print('54. 智能问诊界面—— → ：')

# Line 633: "安全指标的验证如果每次都靠人工逐条检查，既耗时又容易遗漏——为此我们编写了一套基于规则匹配的自动评测脚本"
# Actually line 633 starts "安全指标的验证..." Let me check
old = '安全指标的验证如果每次都靠人工逐条检查，既耗时又容易遗漏。为此我们编写了一套基于规则匹配的自动评测脚本'
old_dash = '安全指标的验证如果每次都靠人工逐条检查，既耗时又容易遗漏——为此我们编写了一套基于规则匹配的自动评测脚本'
if old_dash in content:
    content = content.replace(old_dash, old); fixes += 1; print('55. 容易遗漏—— → 。')

# Line 641: "因为它面临的问题在三个模块中最为困难——" → Let me check
old = 'OCR模块占据最多篇幅——因为它面临的问题在三个模块中最为困难'
# Check
old_alt = 'OCR模块占据最多篇幅，因为它面临的问题在三个模块中最为困难'
old_dash_alt = 'OCR模块占据最多篇幅——因为它面临的问题在三个模块中最为困难'
if old_dash_alt in content:
    content = content.replace(old_dash_alt, old_alt); fixes += 1; print('56. 最多篇幅—— → ，')

# Line 643: "明确告知用户数据量尚不足以进行趋势分析——在健康场景下" → KEEP

# Line 645: "每个环节的选型都绕不开同一个问题：在医疗场景下，可控和安全优先于省事和抽象"
# Wait, this already uses "："? Let me check the exact text
old_dash_645 = '每个环节的选型都绕不开同一个问题——在医疗场景下，可控和安全优先于省事和抽象'
new_645 = '每个环节的选型都绕不开同一个问题：在医疗场景下，可控和安全优先于省事和抽象'
if old_dash_645 in content:
    content = content.replace(old_dash_645, new_645); fixes += 1; print('57. 同一个问题—— → ：')

# ============================================================
# CHAPTER 5: 系统测试与评测 (original ~20 dashes, target ~5-6)
# ============================================================

# Line 655: "速度快、确定性强——每次git commit前自动运行一轮"
old = '这层测试的优势在于速度快、确定性强——每次git commit前自动运行一轮，十余秒即可检测是否存在明显的回归错误'
new = '这层测试的优势在于速度快、确定性强：每次git commit前自动运行一轮，十余秒即可检测是否存在明显的回归错误'
if old in content:
    content = content.replace(old, new); fixes += 1; print('58. 确定性强—— → ：')

# Line 657: "每个测试用例拥有自己独立的数据库实例——用例之间不会彼此污染"
old = '每个测试用例拥有自己独立的数据库实例——用例之间不会彼此污染，这一原则来源于反复调试实践中积累的经验'
new = '每个测试用例拥有自己独立的数据库实例（用例之间不会彼此污染），这一原则来源于反复调试实践中积累的经验'
if old in content:
    content = content.replace(old, new); fixes += 1; print('59. 数据库实例—— → （）')

# Line 659: "按用户真实的操作顺序串行执行——注册、登录、OCR、录入、看板、问诊——验证各模块之间"
old = '按用户真实的操作顺序串行执行——注册、登录、OCR、录入、看板、问诊——验证各模块之间的接口契约'
new = '按用户真实的操作顺序串行执行（注册、登录、OCR、录入、看板、问诊），验证各模块之间的接口契约'
if old in content:
    content = content.replace(old, new); fixes += 1; print('60. 串行执行...问诊—— → （）')

# Line 661: "实际发现的交互问题较多——特别是各类操作流程" → KEEP
# Line 665: "累计执行时间约11秒——可满足快速回归测试的需求" → KEEP
# Line 667: "三个核心服务模块...覆盖率都超过90\%——这一点尤为重要" → KEEP
# Line 673: "这是时间约束下的取舍——在前后端并行推进的项目中" → KEEP

# Line 706: "表明RAG在统计上显著优于...基线LLM——本系统的评测结果与该Meta分析的总体结论方向一致" → KEEP

# Line 708: "在数据极度稀疏的场景...模型的表现是符合预期的——它明确说了" → ，
old = '模型的表现是符合预期的——它明确说了"仅1条记录无法反映趋势'
new = '模型的表现是符合预期的，它明确说了"仅1条记录无法反映趋势'
if old in content:
    content = content.replace(old, new); fixes += 1; print('61. 符合预期的—— → ，')

# Line 710: "被高频引用的文档集中在...这几篇——这个分布符合预期"
old = '被高频引用的文档集中在高血压阈值与分级、家庭测量规范、急诊识别和常见问答这几篇——这个分布符合预期'
new = '被高频引用的文档集中在高血压阈值与分级、家庭测量规范、急诊识别和常见问答这几篇，这个分布符合预期'
if old in content:
    content = content.replace(old, new); fixes += 1; print('62. 这几篇—— → ，')

# Line 712: "无法评估回答的临床准确性和建议质量——后者仍需人工审阅"
old = '但无法评估回答的临床准确性和建议质量——后者仍需人工审阅'
new = '但无法评估回答的临床准确性和建议质量，后者仍需人工审阅'
if old in content:
    content = content.replace(old, new); fixes += 1; print('63. 建议质量—— → ，')

# Line 739: "本文双通路方案在100\%准确率的前提下平均耗时1.00秒，满足3秒的性能约束——分类器决策耗时不足1毫秒"
old = '满足3秒的性能约束——分类器决策耗时不足1毫秒'
new = '满足3秒的性能约束（分类器决策耗时不足1毫秒'
if old in content:
    # But need closing paren. Let me check the full sentence
    old_full = '本文双通路方案在100\\%准确率的前提下平均耗时1.00秒，满足3秒的性能约束——分类器决策耗时不足1毫秒，LCD图片经VLM端到端识别约1.05秒，标准字体图片经百度云OCR约0.64秒。'
    new_full = '本文双通路方案在100\\%准确率的前提下平均耗时1.00秒，满足3秒的性能约束（分类器决策耗时不足1毫秒，LCD图片经VLM端到端识别约1.05秒，标准字体图片经百度云OCR约0.64秒）。'
    if old_full in content:
        content = content.replace(old_full, new_full); fixes += 1; print('64. 性能约束—— → （）')

# Line 741: "主要误差来源为极端反光条件下个别字段的OCR漏检——该问题已在VLM兜底机制中有所缓解" → KEEP

# Line 764: "单次耗时约250毫秒，这是有意选择的参数——该延迟在用户体验可接受范围内" → KEEP
# Line 788: "SSE首Token的P95延迟为1.50秒，远低于3秒的设计约束——" → KEEP? Let me check
# Actually the text is: "SSE首Token的P95延迟为1.50秒，远低于3秒的设计约束" — this might not have a dash. Let me check the grep output.

# Line 792: "十余秒即可完成回归检测——对于需要频繁迭代OCR流水线和Prompt模板的开发节奏而言" → KEEP
# Line 798: "越权访问一律返回404（刻意不用403，原因在3.3节已说明）" → uses parens already, fine

# ============================================================
# CHAPTER 6: 结论与展望 (original ~14 dashes, target ~6-7)
# ============================================================

# Line 824: "以下几个方面的不足也需要正视——有些是受限于时间和资源" → KEEP
# Line 826: "还是不够——用二项分布估算" → KEEP
# Line 828: "不易被替代的优点——结果高度透明" → KEEP
# Line 830: "本质上是'软'的——它们是要求大模型遵守的规则" → KEEP
# Line 832: "移动端的响应式适配也未实现——对于一个目标用户包含大量手机端操作场景的系统来说" → KEEP
# Line 834: "最终仍需依赖真实用户在实际家庭环境中的使用体验和反馈——目前仍缺少这一环节" → KEEP
# Line 838: "继续推进——按优先级排列" → KEEP

# Line 840: "建立标准化的评测基准——没有足够规模的测试集" → KEEP
# But check if this is actually in the text with a dash:
old = '建立标准化的评测基准——没有足够规模的测试集'
if old in content:
    KEEP_840 = True  # already keeping
    pass  # KEEP - important

# Line 842: "后续应当支持增量更新、变更追踪和回滚——至少能明确"
old = '后续应当支持增量更新、变更追踪和回滚——至少能明确"当前知识库版本、最近更新时间与变更内容"'
new = '后续应当支持增量更新、变更追踪和回滚，至少能明确"当前知识库版本、最近更新时间与变更内容"'
if old in content:
    content = content.replace(old, new); fixes += 1; print('65. 变更追踪和回滚—— → ，')

# Line 848: "Docker Compose生产环境、Nginx反向代理+HTTPS、CI/CD流水线、数据库定时备份和日志轮转——这些在开发阶段尚未完成的工程化工作需要补上"
old = 'Docker Compose生产环境、Nginx反向代理+HTTPS、CI/CD流水线、数据库定时备份和日志轮转——这些在开发阶段尚未完成的工程化工作需要补上'
new = 'Docker Compose生产环境、Nginx反向代理+HTTPS、CI/CD流水线、数据库定时备份和日志轮转，这些在开发阶段尚未完成的工程化工作需要补上'
if old in content:
    content = content.replace(old, new); fixes += 1; print('66. 日志轮转—— → ，')

# Line 850: "本质上是'软约束'——LLM生成的文本" → KEEP
# Line 852: "但至少验证了——"
old = '但它至少验证了：将OCR、VLM、RAG和时序分析这几项技术整合起来为普通家庭服务'
old_dash = '但它至少验证了——将OCR、VLM、RAG和时序分析这几项技术整合起来为普通家庭服务'
if old_dash in content:
    content = content.replace(old_dash, old); fixes += 1; print('67. 验证了—— → ：')

# Line 852: "没有真实用户的反馈，上述判断均属于待验证的假设"
# Check if this has a dash
old2 = '没有真实用户的反馈，上述判断均属于待验证的假设。'
old_dash2 = '没有真实用户的反馈——上述判断均属于待验证的假设。'
if old_dash2 in content:
    content = content.replace(old_dash2, old2); fixes += 1; print('68. 用户反馈—— → ，')

# ============================================================
# Fix em-dashes in parenthetical that should be commas or colons
# (一些可能遗漏的通用模式)
# ============================================================

# Check for remaining dashes and try common patterns
# "——这是" → often replaceable → keep if important, replace if casual
# "——即" → ：
# "——因为" → ，

# Let's handle some patterns that might have been missed
patterns = [
    # Line 244 already handled as KEEP
    # Additional cleanups for phrases that slipped through
]

# Save
with open(r'd:\HealthAgent\docs\thesis.tex', 'w', encoding='utf-8') as f:
    f.write(content)

new_count = content.count('——')
print(f'\nTotal replacements: {fixes}')
print(f'Em-dashes: {orig_count} -> {new_count} (removed {orig_count - new_count})')
