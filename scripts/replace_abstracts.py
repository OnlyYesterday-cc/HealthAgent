#!/usr/bin/env python3
"""Replace abstracts with shorter versions and trim body text (PRESERVING all citations)"""
import sys

with open(r'd:\HealthAgent\docs\thesis.tex', 'r', encoding='utf-8') as f:
    content = f.read()

orig = content.count('\n')
print(f'Original: {orig} lines')
fixes = 0

# ===== 1. CHINESE ABSTRACT =====
old_cn = (
    '我国成年人高血压患病率约为27.9\\%，患者总数超过2.45亿人，但知晓率、治疗率和控制率分别仅为51.6\\%、'
    '45.8\\%和16.8\\%，绝大多数患者未能实现有效的血压管理。家用电子血压计已较为普及，然而测量后的数据记录、'
    '趋势解读和健康咨询等环节普遍缺失：手写记录难以长期保存与回顾，现有健康管理应用多停留在数据可视化层面而'
    '缺乏针对性解读，网络健康信息质量参差不齐，普通用户难以甄别。光学字符识别、大语言模型与检索增强生成等'
    '人工智能技术的快速发展，为构建面向普通家庭的智能化血压管理工具提供了新的技术条件。\n\n'
    '针对上述问题，设计并实现了一款名为HealthAgent的个人健康管理智能体，围绕"拍照记录血压、看图理解趋势、'
    '对话获取建议"三项核心功能展开。在血压计图像识别方面，提出并实现了一种分类先行的双通路光学字符识别方案：'
    '首先由本地方向梯度直方图+支持向量机分类器判定图像为七段数码管液晶显示屏或标准印刷字体界面，前者直接路由'
    '至视觉语言大模型完成端到端识别，后者经由百度云通用光学字符识别接口配合X坐标聚类完成字段抽取与分配。'
    '在健康数据管理方面，实现了用户级数据隔离、基于自适应窗口的滑动平均趋势判定算法以及双Y轴交互式时序看板。'
    '在智能问诊方面，以12篇医学知识文档构建向量知识库，基于sqlite-vec扩展实现本地向量存储与语义检索，将用户'
    '近14天血压概况与检索到的知识片段嵌入Prompt，通过通义千问大模型生成个性化回复，采用服务器推送事件协议实现'
    '流式逐字输出。系统指令中内嵌六条安全行为边界——禁止推荐药物剂量、禁止确定性诊断、强制引用标注与免责声明等，'
    '并在模型输出侧辅以规则引擎进行高危模式扫描。系统后端基于Python FastAPI框架与SQLite数据库构建，前端采用'
    'React 18、TypeScript、Ant Design 5与ECharts技术栈，以JSON Web令牌双Token机制实现身份认证。\n\n'
    '在20张血压计图像（10张七段数码管液晶显示屏与10张标准印刷字体，共计60个标注字段）上的统一评测表明，'
    '该双通路方案在两类图像上的端到端字段识别准确率均达到100.0\\%，而四种纯光学字符识别基线方案在七段数码管'
    '场景下的准确率均不足20\\%。检索增强生成问诊模块的三项安全指标——引用标注率、免责声明率和剂量安全率'
    '——经由自动评测脚本在10道典型问题上验证均达到100\\%。后端86个测试用例全部通过，代码覆盖率为82\\%；'
    '前端15个测试用例全部通过，TypeScript严格模式下无类型错误。'
)

# Check if this long abstract exists
if old_cn in content:
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
    fixes += 1
    print('1. Chinese abstract replaced OK')
else:
    print('1. WARNING: CN abstract pattern NOT FOUND - trying split approach')
    # Split into parts for matching
    part1 = '我国成年人高血压患病率约为27.9\\%'
    if part1 in content:
        print('  -> Found shorter CN abstract already in place')
    else:
        print('  -> Unknown CN abstract format')

# ===== 2. ENGLISH ABSTRACT =====
old_en = (
    'Hypertension affects approximately 27.9\\% of Chinese adults, totaling over 245 million patients, '
    'yet the awareness, treatment, and control rates stand at only 51.6\\%, 45.8\\%, and 16.8\\%, '
    'respectively—meaning the vast majority of patients do not achieve effective blood pressure management. '
    'While home blood pressure monitors are widely available, the downstream tasks of data recording, '
    'trend interpretation, and health consultation remain largely unaddressed: handwritten records are '
    'difficult to preserve and review, existing health applications seldom go beyond data visualization '
    'to offer personalized insights, and the quality of online health information varies considerably, '
    'making it difficult for non-experts to distinguish reliable guidance from misinformation. '
    'Recent advances in Optical Character Recognition (OCR), Large Language Models (LLMs), and '
    'Retrieval-Augmented Generation (RAG) present an opportunity to build intelligent, accessible tools '
    'for home-based blood pressure management.\n\n'
    'To address this gap, HealthAgent, a personal health management agent, was designed and implemented '
    'around three core capabilities: photographing blood pressure readings, viewing trends via a dashboard, '
    'and consulting an AI that grounds its answers in medical references. '
)

if old_en in content:
    # Find the full old English abstract
    en_start_str = 'Hypertension affects approximately 27.9\\% of Chinese adults'
    en_start = content.find(en_start_str)
    en_end_str = 'zero TypeScript strict-mode errors.'
    en_end = content.find(en_end_str, en_start)
    if en_end > 0:
        en_end += len(en_end_str)
        full_old_en = content[en_start:en_end]

        new_en = (
            'The prevalence of hypertension in China remains high, yet the rates of awareness, treatment, '
            'and control are all at low levels. Although home blood pressure monitors have become widely available, '
            'critical downstream tasks—data recording, trend interpretation, and health consultation—remain largely '
            'unaddressed. Recent advances in Optical Character Recognition (OCR) and Large Language Models (LLMs) '
            'present an opportunity to close this gap.\n\n'
            'To address these challenges, HealthAgent, a personal health management agent, was designed and '
            'implemented around three core capabilities: photographing readings, understanding trends via a dashboard, '
            'and consulting an AI grounded in medical references. For image recognition, a classification-first '
            'dual-pathway OCR scheme was proposed: a local HOG+SVM classifier determines whether the image depicts '
            'a seven-segment LCD screen or a standard printed-font interface, routing LCD images directly to a '
            'Vision-Language Model for end-to-end recognition, while standard-font images are processed via the '
            'Baidu Cloud OCR API with X-coordinate clustering for field extraction. For health data management, '
            'per-user data isolation, an adaptive-window trend assessment algorithm, and an interactive dual Y-axis '
            'dashboard were implemented. For the intelligent consultation module, a vector knowledge base was '
            'constructed from curated medical documents; each query prompt embeds the user\'s recent blood pressure '
            'summary alongside retrieved knowledge chunks, with responses generated by an LLM and streamed '
            'token-by-token via Server-Sent Events. Six safety constraints—prohibiting dosage recommendations and '
            'diagnostic conclusions, and mandating source citations and disclaimers—are embedded in the system, '
            'supplemented by a rule engine that scans for high-risk patterns. The backend is built on FastAPI and '
            'SQLite, while the frontend employs React, TypeScript, Ant Design, and ECharts, with JWT dual-token '
            'authentication.\n\n'
            'Evaluation demonstrates that the dual-pathway scheme achieves complete and accurate recognition on '
            'both image categories, whereas pure-OCR baselines perform markedly worse on seven-segment LCD inputs. '
            'All three safety metrics of the RAG consultation module meet compliance thresholds, and both backend '
            'and frontend test suites pass in full.'
        )
        content = content.replace(full_old_en, new_en)
        fixes += 1
        print('2. English abstract replaced OK')
    else:
        print('2. EN abstract end not found')
else:
    # Maybe already the shorter version?
    if 'The prevalence of hypertension in China remains high' in content:
        print('2. EN abstract already replaced')
    else:
        print('2. WARNING: EN abstract pattern NOT FOUND')
        # Show what's there
        idx = content.find('Hypertension affects')
        if idx > 0:
            print(f'   Found at {idx}: {repr(content[idx:idx+80])}')

# ===== SAVE =====
with open(r'd:\HealthAgent\docs\thesis.tex', 'w', encoding='utf-8') as f:
    f.write(content)

final = content.count('\n')
print(f'\nFixes applied: {fixes}')
print(f'Lines: {orig} -> {final}')
