#!/usr/bin/env python3
"""Second pass: reduce remaining em-dashes that were missed in first pass."""
import re

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

orig_count = content.count('——')
print(f'Starting em-dash count: {orig_count}')
fixes = 0

# ===== Chapter 1 =====

# Line 246: "字体样本——这种字体" -> ，
old = '几乎没有包含七段数码管这类字体样本——这种字体在通用OCR的训练语料中占比极低'
new = '几乎没有包含七段数码管这类字体样本，这种字体在通用OCR的训练语料中占比极低'
if old in content:
    content = content.replace(old, new); fixes += 1; print('1. 字体样本—— → ，')

# ===== Chapter 2 =====

# Line 286: "临时知识注入——模型不需要" -> ：
old = '做一次"临时知识注入"——模型不需要在训练阶段记住所有医学信息'
new = '做一次"临时知识注入"：模型不需要在训练阶段记住所有医学信息'
if old in content:
    content = content.replace(old, new); fixes += 1; print('2. 临时知识注入—— → ：')

# Line 288: "重新训练模型——这在医学" -> ，
old = '修改后即可生效，无需重新训练模型——这在医学场景下意味着'
new = '修改后即可生效，无需重新训练模型，这在医学场景下意味着'
if old in content:
    content = content.replace(old, new); fixes += 1; print('3. 重新训练模型—— → ，')

# Line 320: "端到端识别——实验已证明" -> ，
old = 'LCD路径上则直接调用通义千问VLM做端到端识别——实验已证明这是目前应对七段数码管字形的最有效手段'
new = 'LCD路径上则直接调用通义千问VLM做端到端识别，实验已证明这是目前应对七段数码管字形的最有效手段'
if old in content:
    content = content.replace(old, new); fixes += 1; print('4. 端到端识别—— → ，')

# Line 322: "X坐标聚类——将X坐标" -> ：
old = '其次优先尝试X坐标聚类——将X坐标相近的token归为'
new = '其次优先尝试X坐标聚类：将X坐标相近的token归为'
if old in content:
    content = content.replace(old, new); fixes += 1; print('5. X坐标聚类—— → ：')

# Line 344: "async/await——这对" -> ，
old = '同时原生支持async/await——这对需要并发等待百度云OCR和DashScope大模型返回的场景具有实际价值'
new = '同时原生支持async/await，这对需要并发等待百度云OCR和DashScope大模型返回的场景具有实际价值'
if old in content:
    content = content.replace(old, new); fixes += 1; print('6. async/await—— → ，')

# Line 346: "服务进程——安装、配置" -> ，
old = 'MySQL和PostgreSQL需要独立的服务进程——安装、配置、权限管理、日常运维均有门槛'
new = 'MySQL和PostgreSQL需要独立的服务进程，其安装、配置、权限管理、日常运维均有门槛'
if old in content:
    content = content.replace(old, new); fixes += 1; print('7. 服务进程—— → ，其')

# Line 348: "Ant Design 5——它的ConfigProvider" -> ，
old = '组件库用了Ant Design 5——它的ConfigProvider主题定制机制可以在全局统一设Design Token'
new = '组件库用了Ant Design 5，它的ConfigProvider主题定制机制可以在全局统一设Design Token'
if old in content:
    content = content.replace(old, new); fixes += 1; print('8. Ant Design 5—— → ，')

# ===== Chapter 3 =====

# Line 362: "这一判断——绝大多数应用" -> ：
old = '系统综述也印证了这一判断——绝大多数应用仅提供数据可视化，缺乏预测和趋势分析功能'
new = '系统综述也印证了这一判断：绝大多数应用仅提供数据可视化，缺乏预测和趋势分析功能'
if old in content:
    content = content.replace(old, new); fixes += 1; print('9. 这一判断—— → ：')

# Line 370: Three dashes
old = '但不希望给父母增添过多操作负担——他们往往是App的实际安装者和初始配置者'
new = '但不希望给父母增添过多操作负担，他们往往是App的实际安装者和初始配置者'
if old in content:
    content = content.replace(old, new); fixes += 1; print('10. 操作负担—— → ，')

old = '有各种具体的问题——"早上测还是晚上测？""测之前能喝咖啡吗？""140算不算高？"——通常不会专门为这些问题挂号就诊'
new = '有各种具体的问题（"早上测还是晚上测？""测之前能喝咖啡吗？""140算不算高？"），通常不会专门为这些问题挂号就诊'
if old in content:
    content = content.replace(old, new); fixes += 1; print('11. 具体的问题...算高？—— → （）')

# Line 376: Two dashes
old = '所有用户数据严格按user\\_id隔离——跨用户访问统一返回HTTP 404而非403'
new = '所有用户数据严格按user\\_id隔离：跨用户访问统一返回HTTP 404而非403'
if old in content:
    content = content.replace(old, new); fixes += 1; print('12. user_id隔离—— → ：')

# Try without backslash
old = '所有用户数据严格按user_id隔离——跨用户访问统一返回HTTP 404而非403'
new = '所有用户数据严格按user_id隔离：跨用户访问统一返回HTTP 404而非403'
if old in content:
    content = content.replace(old, new); fixes += 1; print('12b. user_id隔离—— → ：')

old = '后端单元测试覆盖率不低于70\\%——该数值对于需要频繁迭代Prompt和OCR流水线的项目而言是一个务实的目标'
new = '后端单元测试覆盖率不低于70\\%，该数值对于需要频繁迭代Prompt和OCR流水线的项目而言是一个务实的目标'
if old in content:
    content = content.replace(old, new); fixes += 1; print('13. 覆盖率不低于70%—— → ，')

# ===== Chapter 3 - database =====

# Line 401: Two dashes
old = '前端用这个来渲染引用来源卡片——用户点一下就能看到回答参考了哪篇文献的哪个段落'
new = '前端用这个来渲染引用来源卡片，用户点一下就能看到回答参考了哪篇文献的哪个段落'
if old in content:
    content = content.replace(old, new); fixes += 1; print('14. 引用来源卡片—— → ，')

old = '主要是为了减少部署复杂度——少一个需要运维的中间件，家庭场景下的系统就更可能被实际用起来'
new = '主要是为了减少部署复杂度：少一个需要运维的中间件，家庭场景下的系统就更可能被实际用起来'
if old in content:
    content = content.replace(old, new); fixes += 1; print('15. 减少部署复杂度—— → ：')

# ===== Chapter 3 - error response =====
# Line 421 area: "转换——转换为" (from the grep omitted match)
# Check for this pattern
old = '所有异常在接口层被统一捕获——转换为固定格式的JSON错误响应'
new = '所有异常在接口层被统一捕获，转换为固定格式的JSON错误响应'
if old in content:
    content = content.replace(old, new); fixes += 1; print('16. 统一捕获—— → ，')

# ===== Chapter 4 =====

# Line 534: Two dashes
old = '\\textbf{第一层：角色与任务描述。}Prompt以明确的任务声明开头——"你是一个医疗设备屏幕读数识别助手'
new = '\\textbf{第一层：角色与任务描述。}Prompt以明确的任务声明开头："你是一个医疗设备屏幕读数识别助手'
if old in content:
    content = content.replace(old, new); fixes += 1; print('17. 任务声明开头—— → ：')

old = '降低了模型试图对数值进行临床解读的倾向——在前期实验中，我们观察到如果不加角色限定'
new = '降低了模型试图对数值进行临床解读的倾向；在前期实验中，我们观察到如果不加角色限定'
if old in content:
    content = content.replace(old, new); fixes += 1; print('18. 临床解读的倾向—— → ；')

# Line 547: "优先级信号——低置信度字段" -> ：
old = '为后续的人机协同审核提供优先级信号——低置信度字段在前端表单中以橙色边框高亮'
new = '为后续的人机协同审核提供优先级信号：低置信度字段在前端表单中以橙色边框高亮'
if old in content:
    content = content.replace(old, new); fixes += 1; print('19. 优先级信号—— → ：')

# Line 549: "负向约束的必要性——在健康场景下" -> ：
old = '但这次对比足以说明负向约束的必要性——在健康场景下，坦诚说"看不清"远比给出一个看似正确但实际错误的数值安全'
new = '但这次对比足以说明负向约束的必要性：在健康场景下，坦诚说"看不清"远比给出一个看似正确但实际错误的数值安全'
if old in content:
    content = content.replace(old, new); fixes += 1; print('20. 负向约束的必要性—— → ：')

# Line 608: Two dashes
old = '源于Lewis等人\\textsuperscript{[20]}提出的检索增强生成（RAG）框架——将外部知识检索与语言模型生成解耦'
new = '源于Lewis等人\\textsuperscript{[20]}提出的检索增强生成（RAG）框架：将外部知识检索与语言模型生成解耦'
if old in content:
    content = content.replace(old, new); fixes += 1; print('21. RAG框架—— → ：')

old = '选取Top-5是基于实验结果确定的——Top-3在部分情况下会遗漏相关内容'
new = '选取Top-5是基于实验结果确定的：Top-3在部分情况下会遗漏相关内容'
if old in content:
    content = content.replace(old, new); fixes += 1; print('22. 实验结果确定的—— → ：')

# Line 620: "引用来源卡片——用户在回答" -> ，
old = '前端收到后立刻渲染引用来源卡片——用户在回答正文出来之前就能看到回答参考了哪些文献'
new = '前端收到后立刻渲染引用来源卡片，用户在回答正文出来之前就能看到回答参考了哪些文献'
if old in content:
    content = content.replace(old, new); fixes += 1; print('23. 引用来源卡片—— → ，')

# ===== Chapter 4 summary =====

# Line 641: "OCR模块占据最多篇幅——因为它" -> ，
old = 'OCR模块占据最多篇幅——因为它面临的问题在三个模块中最为困难'
new = 'OCR模块占据最多篇幅，因为它面临的问题在三个模块中最为困难'
if old in content:
    content = content.replace(old, new); fixes += 1; print('24. 最多篇幅—— → ，')

# ===== Chapter 5 =====

# Line 788: Check what the dash is here. From the Read, it might be about SSE delay
# Let me check with a broader context
old = 'SSE首Token的P95延迟为1.50秒，远低于3秒的设计约束——用户在对话界面感知到的'
new = 'SSE首Token的P95延迟为1.50秒，远低于3秒的设计约束，用户在对话界面感知到的'
if old in content:
    content = content.replace(old, new); fixes += 1; print('25. 设计约束—— → ，')

# ===== Chapter 6 =====

# Line 840: "最新进展——这两个方向也为" -> ，
old = '系统梳理了AI在血压预测、风险分层、可穿戴监测和个性化干预中的最新进展——这两个方向也为OCR模块的未来迭代提供了可参考的技术路径'
new = '系统梳理了AI在血压预测、风险分层、可穿戴监测和个性化干预中的最新进展，这两个方向也为OCR模块的未来迭代提供了可参考的技术路径'
if old in content:
    content = content.replace(old, new); fixes += 1; print('26. 最新进展—— → ，')

# Line 852: "聊天获建议——这三个环节" -> Keep? This is the tagline...
# Actually the user might want this kept, but it's paratactic enumeration. Let me replace with ： for consistency.
old = '聊天获建议——这三个环节串联起来，构成了从数据采集到行动决策的完整小闭环'
new = '聊天获建议：这三个环节串联起来，构成了从数据采集到行动决策的完整小闭环'
if old in content:
    content = content.replace(old, new); fixes += 1; print('27. 聊天获建议—— → ：')

# Save
with open(r'd:\HealthAgent\docs\thesis.tex', 'w', encoding='utf-8') as f:
    f.write(content)

new_count = content.count('——')
print(f'\nTotal replacements: {fixes}')
print(f'Em-dashes: {orig_count} -> {new_count} (removed {orig_count - new_count})')
